import sys
import math
import random
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import treelib
from pandas.core.frame import DataFrame
from scipy.spatial import distance_matrix
from sklearn.manifold import MDS
from treelib.node import Node
from treelib.tree import Tree


def getICD10GMTree():
    """
    Returns a tree that represents the ICD10 taxonomy. \n
    Based on the ICD10-XML export from https://www.dimdi.de/dynamic/de/klassifikationen/downloads/
    """
    raw_xml = ET.parse('resources\\ICD10_xml.xml')
    root = raw_xml.getroot()
    tree = treelib.Tree()
    tree.create_node('ICD-10', 0)

    # create all nodes
    for clss in root.iter('Class'):
        tree.create_node(clss.get('code'), clss.get('code'), parent=0)

    # move them to represent the hierarchy
    for clss in root.iter('Class'):
        if clss.get('kind') != 'chapter':
            for superclass in clss.iter('SuperClass'):
                tree.move_node(clss.get('code'), superclass.get('code'))

    return tree

def getIC(code, tree: Tree, ic_mode: str):
    """
    Returns information content of a given code 
    based on the IC algorthms from https://doi.org/10.1186/s12911-019-0807-y
    
    """
    try:
        if ic_mode == 'levels':
            # IC calculation based on Boriah et al. https://doi.org/10.1137/1.9781611972788.22 
            return tree.depth(code)
        elif ic_mode == 'ontology':
            return getSanchezIC(code,tree)
        else:
            raise ValueError('Unsupported IC-mode',ic_mode)
    except ValueError as err:
        print(err.args)
        sys.exit()

def getSanchezIC(code: str, tree: Tree):
    """IC calculation based on Sánchez et al. https://doi.org/10.1016/j.knosys.2010.10.001"""
    leaves_cnt = len(tree.leaves(code))
    ancestors_cnt = len(getAncestors(code,tree))
    return -math.log( (leaves_cnt/ancestors_cnt + 1)/(leaves_cnt+1) )

def getLCA(code1, code2, tree, ic_mode):
    """Return lowest common ancester of two codes."""
    lca = 0
    ca = list(getAncestors(code1, tree).intersection(getAncestors(code2, tree)))
    if len(ca) != 0:
        lca = ca[0]
        for code in ca:
            if getIC(code, tree, ic_mode) > getIC(lca, tree, ic_mode):
                lca = code
    return lca


def getAncestors(code, tree: Tree):
    """Return the ancestors of a code in a given tree"""
    ancestors = []
    parent: Node = tree.parent(code)
    while tree.depth(parent.identifier) >= 1:
        ancestors.append(parent.identifier)
        if parent.is_root():
            return set(ancestors)
        parent = tree.parent(parent.identifier)

    return set(ancestors)

def getCSLi(ic_1,ic_2,ic_lca):
    """CS calculation based on Li et al. https://doi.org/10.1109/TKDE.2003.1209005"""
    return 1 - math.exp(0.2*(ic_1 + ic_2 - 2*ic_lca))*(math.exp(0.6*ic_lca)-math.exp(-0.6*ic_lca))/(math.exp(0.6*ic_lca)+math.exp(-0.6*ic_lca))

def getCSWuPalmer(ic_1,ic_2,ic_lca):
    """CS calculation based on Wu et al. https://doi.org/10.3115/981732.981751"""
    return 1 - (2*ic_lca)/(ic_1+ic_2)

def getCSSimpleWuPalmer(ic_lca, depth):
    """
    CS calculation based on a simplified version of Wu-Palmer,
    where the two codes are on the deepest level of the taxonomy tree
    """
    return (depth - ic_lca)/(depth - 1)

def getCS(code1, code2, tree, depth,ic_mode,cs_mode):
    """Returns code similarity of two codes based on CS-algorithms from https://doi.org/10.1186/s12911-019-0807-y"""
    if code1 == code2:
        return 0.0
    lca = getLCA(code1, code2, tree, ic_mode)
    ic_lca = getIC(lca, tree,ic_mode)
    ic_1 = getIC(code1,tree,ic_mode)
    ic_2 = getIC(code2,tree,ic_mode)

    try:
        #CS1
        if cs_mode == 'binary':
            return int(code1==code2)
        # CS2
        elif cs_mode == 'wu_palmer':
            return getCSWuPalmer(ic_1,ic_2,ic_lca) 
        # CS 3
        elif cs_mode == 'li':
            return getCSLi(ic_1,ic_2,ic_lca)
        # CS4
        elif cs_mode == 'simple_wu_palmer':
            return getCSSimpleWuPalmer(ic_lca,depth)
        
        else:
         raise ValueError('Unsupported CS-mode',cs_mode)
    except ValueError as err:
        print(err.args)
        sys.exit()
    
    ###### ONLY >= PYTHON 3.10.0 #####
    # match cs_mode:
    #     # CS1
    #     case 'binary':
    #         return int(code1==code2)
    #     # CS2
    #     case 'wu_palmer':
    #         return 1 - (2*ic_lca)/(ic_1+ic_2) 
    #     # CS 3
    #     case 'li':
    #         return 1 - math.exp( 0.2*(ic_1 + ic_2 - 2*ic_lca) )*
    #     # CS4
    #     case 'simple_wu_palmer':
    #         return (depth - ic_lca)/(depth - 1)


def getAllCodes(tree: Tree):
    all_codes = []
    for node in tree.all_nodes():
        all_codes.append(node.identifier)
    all_codes.remove(0)
    return all_codes

def getDistMatrix(codes: list, tree: Tree, worker_index, max_workers,ic_mode,cs_mode):
    """
    Function for the parallelized processes. \n 
    Computes the part of the (absolute) distance matrix of the given codes, 
    that corresponds to the worker index of the calling process.
    """
    depth = tree.depth()
    length = len(codes)
    start = getStart(worker_index, max_workers, length)
    stop = getStop(worker_index, max_workers, length)
    dist_matrix = np.zeros(shape=(stop-start, length))
    i = 0
    for code1 in codes[start:stop]: 
        code1_index = codes.index(code1)
        for code2 in codes[code1_index:]:
            cs = getCS(code1, code2, tree,depth,ic_mode,cs_mode)
            # safe CS values in matrix (only upper triangular)
            dist_matrix[i, codes.index(code2)] = cs
        i+=1
    return dist_matrix, worker_index

def getDistMatrixSeq(codes: list, tree: Tree, dist_matrix): 
    """Calculates the (absolute) distance matrix of the given codes sequentially""" 
    depth = tree.depth()

    for code1 in codes:
        code1_index = codes.index(code1)
    # calculates only upper-triangular values & writes them to the corresponding diagonal index 
        for code2 in codes[code1_index:]:
            cs = getCS(code1, code2, tree,depth)
            # safe CS values in matrix
            dist_matrix[codes.index(code1), codes.index(code2)] = cs

def getStop(worker_index, max_workers, length):
    """Returns logarithmically spaced stop index"""
    if worker_index == max_workers:
        return length
    return getStart(worker_index + 1, max_workers, length)

def getStart(worker_index, max_workers, length):
    '''Returns logarithmically spaced start index'''
    logspace = getSpacing(max_workers, length)
    return math.ceil(logspace[worker_index-1])

def getSpacing(max_workers, length):
    """Returns spacing for the code list."""
    logspace =  length/10*np.logspace(start=-1,stop=1,num=max_workers, endpoint=True)
    # remove offset
    logspace = logspace - logspace[0] 
    return logspace

def getDistMatrixWrapper(p):
    """Wrapper for the parallel-process-function"""
    return getDistMatrix(*p)

def getMDSMatrix(dist_matrix):
    """Computes multi-dimensionally-scaled two-dimensional code-coordinates based on a pairwise-distance-matrix"""
    # use MDS to compute the relative distances of the distinct codes
    embedding = MDS(n_components=2)
    dist_matrix_transformed = embedding.fit_transform(dist_matrix)

    df_dist_matrix = pd.DataFrame(dist_matrix_transformed)
    return df_dist_matrix

def mirrorMatrix(dist_matrix):
    """mirrors uppertriangular distance matrix along its diagonal"""
    return dist_matrix + dist_matrix.T - np.diag(np.diag(dist_matrix))

def plotCodes(df_mds_coordinates: DataFrame, codes: list):
    fig, ax = plt.subplots()
    df_mds_coordinates.plot(0, 1, kind='scatter', ax=ax)

    for k, v in df_mds_coordinates.iterrows():
        ax.annotate(codes[k], v)

    plt.show()

def saveCodeDistancesInExcel(df_mds_coordinates: DataFrame, codes: list):
    """Saves pairwise code-distances to excel."""
    array = df_mds_coordinates.to_numpy()
    dm = distance_matrix(array,array)
    df = pd.DataFrame(dm)
    df.to_excel('code_distances.xlsx')

def getRandomCodes(code_cnt: int,tree: treelib.Tree) -> list:
    """Returns list with code_cnt random codes from the given taxonomy tree."""
    nodes: list[Node]
    nodes = random.sample(tree.all_nodes(),code_cnt)
    return [x.identifier for x in nodes]

def getCodeCount(tree: treelib.Tree):
    """Returns the number of codes in a taxonomy."""
    return len(tree.leaves())

    