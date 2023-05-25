import math
import sys
import os
sys.path.append(os.getcwd())
from src.taxodist import td_utils as utils
from treelib import Tree
import warnings
from scipy.optimize import linear_sum_assignment
from sklearn import preprocessing

def getJaccardSetSim(concepts_1: set, concepts_2: set):
    """ Returns Jaccard Set Similarity for the given concept sets """
    
    intersection = len(concepts_1.intersection(concepts_2))
    union = len(concepts_1.union(concepts_2))
    if union != 0:
        return float(intersection) / union
    else:
        warnings.warn("Union was zero")
        return 0
    

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
    return intersection/min(len(concepts_1),len(concepts_2))

def getMeanCSSetSim(concepts_1: set, concepts_2: set,tree: Tree, cs_mode:str,ic_mode: str = 'sanchez'):
    ''' Returns Set Similarity based on SS#7 from Jia et al. '''
    sum = 0
    depth = tree.depth()
    for concept_1 in concepts_1:
        for concept_2 in concepts_2:
            sum += utils.getCS(concept_1,concept_2,tree,depth,ic_mode,cs_mode)
    return (sum*0.5)/(len(concepts_1)+len(concepts_2))

def getHierachicalDistSetSim(concepts_1: set, concepts_2: set,tree: Tree, cs_mode:str,ic_mode: str = 'sanchez'):
    """ Returns hierarchical DISTANCE for the given concept sets based on https://doi.org/10.1016/j.jbi.2016.07.021 """
    
    if concepts_1 == concepts_2:
        return 0.0

    difference_1 = concepts_1.difference(concepts_2)
    difference_2 = concepts_2.difference(concepts_1)
    union = concepts_1.union(concepts_2)
    depth = tree.depth()

    # NOTE commented out the sim/dist differences, because MAX_CS 
    #      takes too much fucking timmmmeee to calculate & normalize (maybe its not even needed)
    
    # # path based = natively used distance measure + other CS-measures that return distances
    # if cs_mode == 'path_based' or cs_mode == 'nguyen_almubaid':
    #     first_summand = sum([utils.getCS(concept_difference_1,concept_2,tree,depth,ic_mode,cs_mode) for concept_2 in concepts_2 for concept_difference_1 in difference_1])
    #     second_summand = sum([utils.getCS(concept_difference_2,concept_1,tree,depth,ic_mode,cs_mode) for concept_1 in concepts_1 for concept_difference_2 in difference_2])
    first_summand = sum([utils.getCS(concept_difference_1,concept_2,tree,depth,ic_mode,cs_mode) for concept_2 in concepts_2 for concept_difference_1 in difference_1])
    second_summand = sum([utils.getCS(concept_difference_2,concept_1,tree,depth,ic_mode,cs_mode) for concept_1 in concepts_1 for concept_difference_2 in difference_2])
    
    # else:
    #     max_cs = utils.getMaxDistOrSim(tree,ic_mode,cs_mode)
    #     # we have to normalize and substract from 1 to turn SIM into DIST measures
    #     first_summand = sum([1 - utils.getCS(concept_difference_1,concept_2,tree,depth,ic_mode,cs_mode)/max_cs for concept_2 in concepts_2 for concept_difference_1 in difference_1])
    #     second_summand = sum([1 - utils.getCS(concept_difference_2,concept_1,tree,depth,ic_mode,cs_mode)/max_cs for concept_1 in concepts_1 for concept_difference_2 in difference_2])

    return ( first_summand/len(concepts_2) + second_summand/len(concepts_1) )/len(union) 

def getWeightedBipartiteMatchingSim(concepts_1: set, concepts_2: set, tree: Tree, ic_mode, cs_mode):
    ''' Weighted undirected bipartite Graph with weight function CS(a,b). 
        Matching = subset of edges with max weights aka highest similarity (or min weights for distance measures) for the two given concept-sets. \n
        Returns max-sum (or min-sum) of the weighted edges. ''' 

    # get pairwise-sim/dist matrix for bipartite matching
    cs_matrix = utils.getCSMatrix(list(concepts_1), list(concepts_2), tree, ic_mode, cs_mode)
    
    # min for distance measures, max for similarity measures
    if cs_mode == "nguyen_almubaid" or cs_mode == "path_based":

        # calculate min distance using hungarian algorithm
        row_ind, col_ind = linear_sum_assignment(cost_matrix=cs_matrix,maximize=False)
    else:

        # calculate max similarity using hungarian algorithm
        row_ind, col_ind = linear_sum_assignment(cost_matrix=cs_matrix,maximize=True)

    return cs_matrix[row_ind, col_ind].sum()


