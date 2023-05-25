from treelib import Tree
import sys
import os
sys.path.append(os.getcwd())
from src.taxodist import td_utils as utils
import math

def getICSanchez(concept: str, tree: Tree):
    """IC calculation based on Sánchez et al. https://doi.org/10.1016/j.knosys.2010.10.001"""
    if concept == tree.root:
        return 0.0
    
    # we have to add 1 to this set, because Sánchez et al. defined the set of subsumer so, 
    # that the concept itself is part of the set
    subsumers = len(utils.getAncestors(concept,tree)) + 1 
    # subsumer(root) = 1 according to Sánchez at el.
    if subsumers == 1:
        return 0.0

    if tree.get_node(concept).is_leaf():
        subtree_leaves_cnt = 0
    else:
        subtree_leaves_cnt = len(tree.leaves(concept))

    all_leaves_cnt = len(tree.leaves()) 
    return -math.log( ( (subtree_leaves_cnt/subsumers) + 1)/(all_leaves_cnt+1) )
