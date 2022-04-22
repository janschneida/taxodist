import math
import td_utils as utils
from treelib import Tree

def getJaccardSetSim(concepts_1: set, concepts_2: set):
    """ Returns Jaccard Set Similarity for the given concept sets """
    intersection = len(concepts_1.intersection(concepts_2))
    union = concepts_1.union(concepts_2)
    return float(intersection) / union

def getDiceSetSim(concepts_1: set, concepts_2: set):
    """ Returns Dice Set Similarity for the given concept sets """
    intersection = len(concepts_1.intersection(concepts_2))
    return (2*intersection)/(len(concepts_2)+len(concepts_1))

def getCosineSetSim(concepts_1: set, concepts_2: set):
    """ Returns Cosine Set Similarity for the given concept sets """
    intersection = len(concepts_1.intersection(concepts_2))
    return intersection/(math.sqrt(len(concepts_2)*len(concepts_1)))

def getOverlapSetSim(concepts_1: set, concepts_2: set):
    """ Returns Overlap Set Similarity for the given concept sets """
    intersection = len(concepts_1.intersection(concepts_2))
    return intersection/min(concepts_1,concepts_2)

def getMeanCSSetSim(concepts_1: set, concepts_2: set,tree: Tree, cs_mode:str,ic_mode: str = 'sanchez'):
    ''' Returns Set Similarity based on SS#7 from Jia et al. '''
    sum = 0
    depth = tree.depth()
    for concept_1 in concepts_1:
        for concept_2 in concepts_2:
            sum += utils.getCS(concept_1,concept_2,tree,depth,ic_mode,cs_mode)
    return sum/(len(concepts_1)*len(concepts_2))

def getHierachicalDistSetSim(concepts_1: set, concepts_2: set,tree: Tree, cs_mode:str,ic_mode: str = 'sanchez'):
    """ Returns hierarchical distance for the given concept sets based on https://doi.org/10.1016/j.jbi.2016.07.021"""
    
    if concepts_1 == concepts_2:
        return 0.0

    difference_1 = concepts_1.difference(concepts_2)
    difference_2 = concepts_2.difference(concepts_1)
    union = concepts_1.union(concepts_2)
    depth = tree.depth()

    first_summand = sum([1 - utils.getCS(concept_difference_1,concept_2,tree,depth,ic_mode,cs_mode) for concept_2 in concepts_2 for concept_difference_1 in difference_1])

    second_summand = sum([1 - utils.getCS(concept_difference_2,concept_1,tree,depth,ic_mode,cs_mode) for concept_1 in concepts_1 for concept_difference_2 in difference_2])

    return ( first_summand/len(difference_2) + second_summand/len(difference_1) )/len(union) 

def getMaxWeightedBipartiteMatching(concepts_1, concepts_2, tree, ic_mode, cs_mode):
    ''' Weighted undirected bipartite Graph with weight function CS(a,b). 
        Matching = subset of edges with max weights aka highest similarity '''
    getAdjacencyMatrix(concepts_1, concepts_2, tree, ic_mode, cs_mode)
    return

def getAdjacencyMatrix(concepts_1, concepts_2, tree, ic_mode, cs_mode):
    return