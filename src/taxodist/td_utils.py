import math
import xml.etree.ElementTree as ET
import numpy as np
from pandas.core.frame import DataFrame
from scipy.spatial import distance_matrix
import treelib
import pandas as pd
# from sklearn.manifold import MDS
# import matplotlib.pyplot as plt
import random

from treelib.node import Node
 
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

def getIC(code, tree):
    """Returns information content (depth) of a given code - based on https://doi.org/10.1186/s12911-019-0807-y"""
    return tree.depth(code)

def getLCA(code1, code2, tree):
    """Return lowest common ancester of two codes."""
    lca = 0
    ca = list(getAncestors(code1, tree).intersection(getAncestors(code2, tree)))
    if len(ca) != 0:
        lca = ca[0]
        for code in ca:
            if getIC(code, tree) > getIC(lca, tree):
                lca = code
    return lca


def getAncestors(code, tree):
    """Return the ancestors of a code in a given tree"""
    ancestors = []
    parent = tree.parent(code)
    while tree.depth(parent.identifier) >= 1:
        ancestors.append(parent.identifier)
        if parent.is_root():
            return set(ancestors)
        parent = tree.parent(parent.identifier)

    return set(ancestors)

def getCS(code1, code2, tree, depth):
    """Returns code similarity of two codes based on CS#4 from https://doi.org/10.1186/s12911-019-0807-y"""
    if code1 == code2:
        return 0.0
    lca = getLCA(code1, code2, tree)
    ic_lca = getIC(lca, tree)
    return (depth - ic_lca) / (depth - 1)


def getAllCodes(tree):
    all_codes = []
    for node in tree.all_nodes():
        all_codes.append(node.identifier)
    all_codes.remove(0)
    return all_codes

def getDistMatrix(ICD10_codes_var, tree, worker_index, max_workers):
    """
    Function for the parallelized processes. \n 
    Computes the part of the (absolute) distance matrix of the given ICD10 codes, 
    that corresponds to the worker index of the calling process.
    """
    depth = tree.depth()
    length = len(ICD10_codes_var)
    start = getStart(worker_index, max_workers, length)
    stop = getStop(worker_index, max_workers, length)
    dist_matrix = np.zeros(shape=(stop-start, length))
    i = 0
    for code1 in ICD10_codes_var[start:stop]: 
        code1_index = ICD10_codes_var.index(code1)
        for code2 in ICD10_codes_var[code1_index:]:
            cs = getCS(code1, code2, tree,depth)
            # safe CS values in matrix (only upper triangular)
            dist_matrix[i, ICD10_codes_var.index(code2)] = cs
        i+=1
    return dist_matrix, worker_index

def getDistMatrixSeq(ICD10_codes_var, tree, dist_matrix): 
    """Calculates the (absolute) distance matrix of the given ICD10 codes sequentially""" 
    depth = tree.depth()

    for code1 in ICD10_codes_var:
        code1_index = ICD10_codes_var.index(code1)
    # calculates only upper-triangular values & writes them to the corresponding diagonal index 
        for code2 in ICD10_codes_var[code1_index:]:
            cs = getCS(code1, code2, tree,depth)
            # safe CS values in matrix
            dist_matrix[ICD10_codes_var.index(code1), ICD10_codes_var.index(code2)] = cs

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
    """Returns spacing for the ICD10 code list."""
    logspace =  length/10*np.logspace(start=-1,stop=1,num=max_workers, endpoint=True)
    # remove offset
    logspace = logspace - logspace[0] 
    return logspace

def getDistMatrixWrapper(p):
    """Wrapper for the parallel-process-function"""
    return getDistMatrix(*p)

def getICD10CodesFromExcel():
    df_raw = pd.read_excel('icd-codes_examples.xlsx', engine='openpyxl')
    df_raw.dropna(inplace=True)
    ICD10_codes = df_raw['ICD-10'].drop_duplicates().to_list()
    ICD10_codes.sort()
    return ICD10_codes


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

def plotCodes(df_mds_coordinates, ICD10_codes):
    fig, ax = plt.subplots()
    df_mds_coordinates.plot(0, 1, kind='scatter', ax=ax)

    for k, v in df_mds_coordinates.iterrows():
        ax.annotate(ICD10_codes[k], v)

    plt.show()

def saveCodeDistancesInExcel(df_mds_coordinates: DataFrame, ICD_10_codes):
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
    return len(tree.leaves()) #TODO fragen: nur leaves oder alle?

    