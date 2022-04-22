import td_utils as utils
import math
from treelib import Tree

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
    return 1-(depth - ic_lca)/depth

def getCSLeacockChodorow(ic_1, ic_2, ic_lca, ic_mode, tree, depth):
    """
    CS calculation based on redefined Leacock Chodorow measure from Sánchez https://doi.org/10.1016/j.jbi.2011.03.013
    """
    global max_ic
    if max_ic is None:
        max_ic = utils.getMaxIC(tree, ic_mode, depth)
    return -math.log((ic_1+ic_2-2*ic_lca+1)/(2*max_ic))

def getCSNguyenAlMubaid(concept1: str, concept2: str, lca: str, tree: Tree, depth: int):
    """ CS calculation based on Nguyen & Al-Mubaid https://doi.org/10.1109/TSMCC.2009.2020689 """
    # TODO add alpha & beta contribution factors
    # TODO lookup reasonable value for k 
    # note: could not find any research on the contribution factors, so we will set them to 1 for now
    depth_lca = tree.level(lca)
    return math.log((utils.getShortestPath(concept1,concept2,depth_lca,tree)-1)*(depth - depth_lca)+1)

def getCSBatet(concept1, concept2, tree):
    """ Cs calculation based on Batet et al. http://dx.doi.org/10.1016/j.jbi.2010.09.002 """
    ancestors_1 = utils.getAncestors(concept1,tree)
    ancestors_1.add(concept1)

    ancestors_2 = utils.getAncestors(concept2,tree)
    ancestors_2.add(concept2)

    shared_ancestors = ancestors_1.intersection(ancestors_2)
    return -math.log2((len(ancestors_1)+len(ancestors_2)-len(shared_ancestors))/(len(ancestors_1)+len(ancestors_2)))