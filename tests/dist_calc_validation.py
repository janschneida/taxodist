import sys
import os
import math
import treelib
sys.path.append(os.getcwd())
from src.taxodist import td_utils as utils

def main():
    """
    Runs tests with different codes to validate the implemented algorithms.\n

    The ground-truth is derived by manually calculating the values for the respective codes.
    """
    tree = getTestTree()
    depth = tree.depth()

    testICs(tree)
    testCSs(tree,depth)

def testCSs(tree, depth):

    
    # WU PALMER TESTS

    cs = utils.getCS(1,1,tree,depth,'level','wu_palmer')
    assert cs == 1.0

    cs = utils.getCS(1,9,tree,depth,'level','wu_palmer')
    assert cs == 0.0

    cs = utils.getCS(13,31,tree,depth,'level','wu_palmer')
    assert math.isclose(cs,0.333,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'level','wu_palmer')
    assert cs == 0.75

    # LI TESTS

    cs = utils.getCS(1,1,tree,depth,'level','li')
    assert cs == 0.0

    cs = utils.getCS(31,31,tree,depth,'level','li')
    assert math.isclose(cs,1.412,rel_tol=0.01)

    cs = utils.getCS(1,9,tree,depth,'level','li')
    assert cs == 0.0

    cs = utils.getCS(13,31,tree,depth,'level','li')
    assert math.isclose(cs,1.195,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'level','li')
    assert math.isclose(cs,1.412,rel_tol=0.01)

    # cs = utils.getCS(70,71,tree,depth,'level','li')
    # assert math.isclose(cs,1.491,rel_tol=0.01)

    # cs = utils.getCS(71,71,tree,depth,'level','li')
    # assert math.isclose(cs,1.491,rel_tol=0.01)

    # SIMPLE WU PALMER TESTS

    cs = utils.getCS(1,1,tree,depth,'level','simple_wu_palmer')
    assert cs == 1.0

    cs = utils.getCS(1,9,tree,depth,'level','simple_wu_palmer')
    assert cs == 0.0

    cs = utils.getCS(13,31,tree,depth,'level','simple_wu_palmer')
    assert math.isclose(cs,0.25,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'level','simple_wu_palmer')
    assert cs == 0.75


def testICs(tree):
    ic = utils.getIC(0,tree,'level')
    assert ic == 0

    ic = utils.getIC(1,tree,'level')
    assert ic == 1

    ic = utils.getIC(10,tree,'level')
    assert ic == 2

    ic = utils.getIC(20,tree,'level')
    assert ic == 3

    ic = utils.getIC(31,tree,'level')
    assert ic == 4

    ic = utils.getIC(0,tree,'sanchez')
    assert ic == 0.0

    ic = utils.getIC(1,tree,'sanchez')
    assert math.isclose(ic,1.386,rel_tol=0.01)

    ic = utils.getIC(10,tree,'sanchez')
    assert math.isclose(ic,2.128,rel_tol=0.01)

    ic = utils.getIC(20,tree,'sanchez')
    assert math.isclose(ic,2.233,rel_tol=0.01)

    ic = utils.getIC(30,tree,'sanchez')
    assert math.isclose(ic,2.639,rel_tol=0.01)

def getTestTree():
    tree = treelib.Tree()
    tree.create_node('test', 0)

    for i in range(1,10):
        tree.create_node(i,i,parent=0)
    
    for i in range (10,14):
        tree.create_node(i,i,parent=1)

    tree.create_node(20,20,parent=10)
    tree.create_node(30,30,parent=20)
    tree.create_node(31,31,parent=20)

    return tree

if __name__ == "__main__":
    main()