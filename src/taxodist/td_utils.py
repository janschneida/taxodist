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

max_ic = None

def getICD_10_GMTree():
    """
    Returns a tree that represents the ICD-10-GM taxonomy. \n
    Based on the ICD-10-XML export from https://www.dimdi.de/dynamic/de/klassifikationen/downloads/
    """
    raw_xml = ET.parse('resources\\ICD_10_xml.xml')
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

def getICD_O_3Tree():
    """
    Returns a tree that represents the ICD-O-3 taxonomy. \n
    Based on the ICD-O-3-XML export from https://www.bfarm.de/DE/Kodiersysteme/Services/Downloads/_node.html
    """
    raw_xml = ET.parse('resources\\ICD_O_3_xml.xml')
    root = raw_xml.getroot()
    tree = treelib.Tree()
    tree.create_node('ICD-O-3', 0)

    # create all nodes
    for clss in root.iter('Class'):
        tree.create_node(clss.get('code'), clss.get('code'), parent=0)

    # move them to represent the hierarchy
    for clss in root.iter('Class'):
        if clss.get('kind') != 'chapter':
            for superclass in clss.iter('SuperClass'):
                tree.move_node(clss.get('code'), superclass.get('code'))

    return tree

def getIC(concept: str, tree: Tree, ic_mode: str):
    """
    Returns information content of a given concept 
    based on the IC algorthms from https://doi.org/10.1186/s12911-019-0807-y
    
    """
    try:
        if ic_mode == 'levels':
            # IC calculation based on Boriah et al. https://doi.org/10.1137/1.9781611972788.22 
            return tree.depth(concept)
        elif ic_mode == 'sanchez':
            return getICSanchez(concept,tree)
        else:
            raise ValueError('Unsupported IC-mode: ',ic_mode)
    except ValueError as err:
        print(err.args)
        sys.exit()

def getICSanchez(concept: str, tree: Tree):
    """IC calculation based on Sánchez et al. https://doi.org/10.1016/j.knosys.2010.10.001"""
    if concept == tree.root:
        return 0.0
    ancestors_cnt = len(getAncestors(concept,tree))
    if ancestors_cnt == 0:
        return 0.0
    subtree_leaves_cnt = len(tree.leaves(concept))
    all_leaves_cnt = len(tree.leaves())
    return -math.log( (subtree_leaves_cnt/ancestors_cnt + 1)/(all_leaves_cnt+1) )


def getLCA(concept1: str, concept2: str, tree: Tree, ic_mode: str) -> str:
    """Return lowest common ancester of two concepts."""
    lca = 0
    ca = list(getAncestors(concept1, tree).intersection(getAncestors(concept2, tree)))
    if len(ca) != 0:
        lca = ca[0]
        for concept in ca:
            # TODO discuss: does this make sense? cant i just take the depth?
            if getIC(concept, tree, ic_mode) > getIC(lca, tree, ic_mode):
                lca = concept
    return lca

def getAncestors(concept, tree: Tree):
    """Return the ancestors of a concept in a given tree"""
    if concept == tree.root:
        return set()
    ancestors = []
    parent: Node = tree.parent(concept)
    while tree.depth(parent.identifier) >= 0:
        ancestors.append(parent.identifier)
        if parent.is_root():
            return set(ancestors)
        parent = tree.parent(parent.identifier)

    return set(ancestors)

def getCSLi(ic_1,ic_2,ic_lca):
    """
    CS calculation based on Li et al. https://doi.org/10.1109/TKDE.2003.1209005
    """
    return math.exp(0.2*(ic_1 + ic_2 - 2*ic_lca))*(math.exp(0.6*ic_lca)-math.exp(-0.6*ic_lca))/(math.exp(0.6*ic_lca)+math.exp(-0.6*ic_lca))

def getCSWuPalmer(ic_1,ic_2,ic_lca):
    """
    CS calculation based on redefined Wu Palmer measure from Sánchez et al. https://doi.org/10.1016/j.jbi.2011.03.013
    Equation is the same as the Lin similarity measure http://dx.doi.org/10.3115/981574.981590
    """
    return (2*ic_lca)/(ic_1+ic_2)

def getCSSimpleWuPalmer(ic_lca, depth):
    """
    CS calculation based on a simplified version of IC-based Wu-Palmer,
    where the two concepts are on the deepest level of the taxonomy tree
    """
    return 1 - (depth - ic_lca)/(depth - 1)

def getCSLeacockChodorow(ic_1, ic_2, ic_lca, ic_mode, tree, depth):
    """
    CS calculation based on redefined Leacock Chodorow measure from Sánchez https://doi.org/10.1016/j.jbi.2011.03.013
    """
    global max_ic
    if max_ic is None:
        max_ic = getMaxIC(tree, ic_mode, depth)
    return -math.log((ic_1+ic_2-2*ic_lca+1)/2*max_ic)

def getCSNguyenAlMubaid(concept1: str, concept2: str, lca: str, tree: Tree, depth: int):
    """ CS calculation based on Nguyen & Al-Mubaid https://doi.org/10.1109/TSMCC.2009.2020689 """
    # TODO add alpha & beta contribution factors
    # TODO lookup reasonable value for k 
    # note: could not find any research on the contribution factors, so we will set them to 1 for now
    depth_lca = tree.level(lca)
    return math.log2((getShortestPath(concept1,concept2,depth_lca,tree)-1)*(depth - depth_lca)+1)

def getCSBatet(concept1, concept2, lca, tree, depth):
    """ Cs calculation based on Batet et al. http://dx.doi.org/10.1016/j.jbi.2010.09.002 """
    ancestors_1 = getAncestors(concept1,tree)
    ancestors_1.add(concept1)

    ancestors_2 = getAncestors(concept2,tree)
    ancestors_2.add(concept2)

    shared_ancestors = ancestors_1.intersection(ancestors_2)
    return -math.log2((len(ancestors_1)+len(ancestors_2)-len(shared_ancestors))/(len(ancestors_1)+len(ancestors_2)))

def getShortestPath(concept1: str, concept2: str, depth_lca: int, tree: Tree):
    depth_concept1 = tree.level(concept1)
    depth_concept2 = tree.level(concept2)
    return depth_concept1 + depth_concept2 - 2*depth_lca

def getCS(concept1: str, concept2: str, tree: Tree, depth: int,ic_mode: str,cs_mode: str):
    """Returns concept similarity of two concepts based on CS-algorithms from https://doi.org/10.1186/s12911-019-0807-y"""
    if concept1 == concept2:
        return 1.0
    lca = getLCA(concept1, concept2, tree, ic_mode)
    ic_lca = getIC(lca, tree,ic_mode)
    ic_1 = getIC(concept1,tree,ic_mode)
    ic_2 = getIC(concept2,tree,ic_mode)
    
    try:
        
        if cs_mode == 'binary':
            return int(concept1==concept2)
        elif cs_mode == 'wu_palmer':
            return getCSWuPalmer(ic_1,ic_2,ic_lca) 
        elif cs_mode == 'li':
            return getCSLi(ic_1,ic_2,ic_lca)
        elif cs_mode == 'simple_wu_palmer':
            return getCSSimpleWuPalmer(ic_lca,depth)
        elif cs_mode == 'leacock_chodorow':
            return getCSLeacockChodorow(ic_1,ic_2,ic_lca,ic_mode,tree,depth)
        elif cs_mode == 'nguyen_almubaid':
            return getCSNguyenAlMubaid(concept1, concept2, lca, tree, depth) 
        elif cs_mode == 'batet_sanchez':
            return getCSBatet(concept1, concept2, lca, tree, depth)        
        else:
         raise ValueError('Unsupported CS-mode: ',cs_mode)
    except ValueError as err:
        print(err.args)
        sys.exit()
    
    ###### ONLY PYTHON >= 3.10.0 #####
    # match cs_mode:
    #     # CS1
    #     case 'binary':
    #         return int(concept1==concept2)
    #     # CS2
    #     case 'wu_palmer':
    #         return 1 - (2*ic_lca)/(ic_1+ic_2) 
    #     # CS 3
    #     case 'li':
    #         return 1 - math.exp( 0.2*(ic_1 + ic_2 - 2*ic_lca) )*
    #     # CS4
    #     case 'simple_wu_palmer':
    #         return (depth - ic_lca)/(depth - 1)


def getAllConcepts(tree: Tree):
    all_concepts = []
    for node in tree.all_nodes():
        all_concepts.append(node.identifier)
    all_concepts.remove(0)
    return all_concepts

def getDistMatrix(concepts: list, tree: Tree, worker_index, max_workers,ic_mode,cs_mode):
    """
    Function for the parallelized processes. \n 
    Computes the part of the (absolute) distance matrix of the given concepts, 
    that corresponds to the worker index of the calling process.
    """
    depth = tree.depth()
    length = len(concepts)
    start = getStart(worker_index, max_workers, length)
    stop = getStop(worker_index, max_workers, length)
    dist_matrix = np.zeros(shape=(stop-start, length))
    i = 0
    for concept1 in concepts[start:stop]: 
        concept1_index = concepts.index(concept1)
        for concept2 in concepts[concept1_index:]:
            cs = getCS(concept1, concept2, tree,depth,ic_mode,cs_mode)
            # safe CS values in matrix (only upper triangular)
            dist_matrix[i, concepts.index(concept2)] = cs
        i+=1
    return dist_matrix, worker_index

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
    """Returns spacing for the concept list."""
    logspace =  length/10*np.logspace(start=-1,stop=1,num=max_workers, endpoint=True)
    # remove offset
    logspace = logspace - logspace[0] 
    return logspace

def getDistMatrixWrapper(p):
    """Wrapper for the parallel-process-function"""
    return getDistMatrix(*p)

def getMDSMatrix(dist_matrix):
    """Computes multi-dimensionally-scaled two-dimensional concept-coordinates based on a pairwise-distance-matrix"""
    # use MDS to compute the relative distances of the distinct concepts
    embedding = MDS(n_components=2)
    dist_matrix_transformed = embedding.fit_transform(dist_matrix)

    df_dist_matrix = pd.DataFrame(dist_matrix_transformed)
    return df_dist_matrix

def mirrorMatrix(dist_matrix):
    """mirrors uppertriangular distance matrix along its diagonal"""
    return dist_matrix + dist_matrix.T - np.diag(np.diag(dist_matrix))

def plotConcepts(df_mds_coordinates: DataFrame, concepts: list):
    fig, ax = plt.subplots()
    df_mds_coordinates.plot(0, 1, kind='scatter', ax=ax)

    for k, v in df_mds_coordinates.iterrows():
        ax.annotate(concepts[k], v)

    plt.show()

def saveConceptDistancesInExcel(df_mds_coordinates: DataFrame, concepts: list):
    """Saves pairwise concept-distances to excel."""
    array = df_mds_coordinates.to_numpy()
    dm = distance_matrix(array,array)
    df = pd.DataFrame(dm)
    df.to_excel('concept_distances.xlsx')

def getRandomConcepts(concept_cnt: int,tree: treelib.Tree) -> list:
    """Returns list with concept_cnt random concepts from the given taxonomy tree."""
    nodes: list[Node]
    nodes = random.sample(tree.all_nodes(),concept_cnt)
    return [x.identifier for x in nodes]

def getConceptCount(tree: treelib.Tree):
    """Returns the number of concepts in a taxonomy."""
    return len(tree.leaves())    

def getMaxIC(tree: Tree, ic_mode: str, depth: int) -> float:
    for node in tree.all_nodes():
        concept = node.identifier
        ancestor_cnt = len(getAncestors(concept, tree))
        if ancestor_cnt == depth:
            return getIC(concept,tree,ic_mode)

def getJaccardSS(concepts_1: set, concepts_2: set):
    """ Returns Jaccard Set Similarity for the given concept sets """
    intersection = len(concepts_1.intersection(concepts_2))
    union = concepts_1.union(concepts_2)
    return float(intersection) / union

def getDiceSS(concepts_1: set, concepts_2: set):
    """ Returns Dice Set Similarity for the given concept sets """
    intersection = len(concepts_1.intersection(concepts_2))
    return (2*intersection)/(len(concepts_2)+len(concepts_1))

def getCosineSS(concepts_1: set, concepts_2: set):
    """ Returns Cosine Set Similarity for the given concept sets """
    intersection = len(concepts_1.intersection(concepts_2))
    return intersection/(math.sqrt(len(concepts_2)*len(concepts_1)))

def getOverlapSS(concepts_1: set, concepts_2: set):
    """ Returns Overlap Set Similarity for the given concept sets """
    intersection = len(concepts_1.intersection(concepts_2))
    return intersection/min(concepts_1,concepts_2)

def getHierachicalDist(concepts_1: set, concepts_2: set,tree: Tree, cs_mode:str,ic_mode: str = 'sanchez'):
    """ Returns hierarchical distance for the given concept sets based on https://doi.org/10.1016/j.jbi.2016.07.021"""
    
    if concepts_1 == concepts_2:
        return 0.0

    difference_1 = concepts_1.difference(concepts_2)
    difference_2 = concepts_2.difference(concepts_1)
    union = concepts_1.union(concepts_2)
    depth = tree.depth()

    first_summand = 0

    for concept_difference_1 in difference_1:
        for concept_2 in concepts_2:
            first_summand += 1 - getCS(concept_difference_1,concept_2,tree,depth,ic_mode,cs_mode)

    second_summand = 0

    for concept_difference_2 in difference_2:
        for concept_1 in concepts_1:
            second_summand += 1 - getCS(concept_difference_2,concept_1,tree,depth,ic_mode,cs_mode)

    return ( (first_summand)/len(difference_2) + (second_summand)/len(difference_1) )/len(union) 