import sys
import os
sys.path.append(os.getcwd())
import math
import treelib
from src.taxodist import td_utils as utils
import unittest

class validation_tests(unittest.TestCase):
    """
    Runs tests with different codes to validate the implemented algorithms.\n

    The ground-truth is derived by manually calculating the values for the respective codes.
    """
    tree = getTestTree()
    depth = tree.depth()

    # testICs(tree)
    testCSs(tree,depth)
    #testSetSims(tree)

def testSetSims(tree):
    
    concepts_1 = (1,2,12,3,31)
    concepts_2 = (1,11)
    concepts_3 = (30,31)

    # BIPARTITE MATCHING TESTS

    setsim = utils.getSetSim(concepts_1, concepts_1,'bipartite_matching', tree, 'wu_palmer','levels')
    assert math.isclose(setsim,5.0,rel_tol=0.01)

    setsim = utils.getSetSim(concepts_1, concepts_2,'bipartite_matching', tree, 'wu_palmer','levels')
    assert math.isclose(setsim,1.5,rel_tol=0.01)

    setsim = utils.getSetSim(concepts_1, concepts_3,'bipartite_matching', tree, 'wu_palmer','levels')
    assert math.isclose(setsim,1.333,rel_tol=0.01)

    setsim = utils.getSetSim(concepts_2, concepts_3,'bipartite_matching', tree, 'wu_palmer','levels')
    assert math.isclose(setsim,0.333,rel_tol=0.01)    

def testCSs(tree, depth):

    # WU PALMER TESTS

    cs = utils.getCS(1,1,tree,depth,'levels','wu_palmer')
    assert cs == 1.0

    cs = utils.getCS(1,9,tree,depth,'levels','wu_palmer')
    assert cs == 0.0

    cs = utils.getCS(13,31,tree,depth,'levels','wu_palmer')
    assert math.isclose(cs,0.333,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'levels','wu_palmer')
    assert cs == 0.75

        cs = utils.getCS(13,31,self.tree,self.depth,'level','wu_palmer')
        self.assertAlmostEqual(cs,0.333,delta=0.001)

    cs = utils.getCS(1,1,tree,depth,'levels','li')
    assert cs == 0.0

    cs = utils.getCS(31,31,tree,depth,'levels','li')
    assert math.isclose(cs,1.412,rel_tol=0.01)

    cs = utils.getCS(1,9,tree,depth,'levels','li')
    assert cs == 0.0

    cs = utils.getCS(13,31,tree,depth,'levels','li')
    assert math.isclose(cs,1.195,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'levels','li')
    assert math.isclose(cs,1.412,rel_tol=0.01)

    # cs = utils.getCS(70,71,tree,depth,'levels','li')
    # assert math.isclose(cs,1.491,rel_tol=0.01)

    # cs = utils.getCS(71,71,tree,depth,'levels','li')
    # assert math.isclose(cs,1.491,rel_tol=0.01)

        # cs = utils.getCS(70,71,self.tree,self.depth,'level','li')
        # assert math.isclose(cs,1.491,rel_tol=0.01)

    cs = utils.getCS(1,1,tree,depth,'levels','simple_wu_palmer')
    assert cs == 1.0

    cs = utils.getCS(1,9,tree,depth,'levels','simple_wu_palmer')
    assert cs == 0.0

    cs = utils.getCS(13,31,tree,depth,'levels','simple_wu_palmer')
    assert math.isclose(cs,0.25,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'levels','simple_wu_palmer')
    assert cs == 0.75

        cs = utils.getCS(13,31,self.tree,self.depth,'level','simple_wu_palmer')
        self.assertAlmostEqual(cs,0.25,delta=0.01)

    cs = utils.getCS(1,1,tree,depth,'sanchez','leacock_chodorow')
    assert math.isclose(cs,0.335,rel_tol=0.01)

    cs = utils.getCS(1,9,tree,depth,'sanchez','leacock_chodorow')
    assert math.isclose(cs,0.022,rel_tol=0.01)

    cs = utils.getCS(13,31,tree,depth,'sanchez','leacock_chodorow')
    assert math.isclose(cs,0.409,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'sanchez','leacock_chodorow')
    assert math.isclose(cs,1.070,rel_tol=0.01)

    cs = utils.getCS(1,1,tree,depth,'levels','leacock_chodorow')
    assert math.isclose(cs,0.980,rel_tol=0.01)

    cs = utils.getCS(1,9,tree,depth,'levels','leacock_chodorow')
    assert math.isclose(cs,0.980,rel_tol=0.01)

    cs = utils.getCS(13,31,tree,depth,'levels','leacock_chodorow')
    assert math.isclose(cs,0.470,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'levels','leacock_chodorow')
    assert math.isclose(cs,0.980,rel_tol=0.01)

        cs = utils.getCS(13,31,self.tree,self.depth,'level','leacock_chodorow')
        self.assertAlmostEqual(cs,0.470,delta=0.001)

    cs = utils.getCS(1,1,tree,depth,'levels','nguyen_almubaid')
    assert math.isclose(cs,1.609,rel_tol=0.01)

    cs = utils.getCS(1,9,tree,depth,'levels','nguyen_almubaid')
    assert math.isclose(cs,1.609,rel_tol=0.01)

    cs = utils.getCS(11,11,tree,depth,'levels','nguyen_almubaid')
    assert math.isclose(cs,1.386,rel_tol=0.01)

    cs = utils.getCS(13,31,tree,depth,'levels','nguyen_almubaid')
    assert math.isclose(cs,2.303,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'levels','nguyen_almubaid')
    assert math.isclose(cs,0.693,rel_tol=0.01)

        cs = utils.getCS(13,31,self.tree,self.depth,'level','nguyen_almubaid')
        self.assertAlmostEqual(cs,2.303,delta=0.001)

    cs = utils.getCS(1,9,tree,depth,'levels','batet')
    assert math.isclose(cs,0.585,rel_tol=0.01)  

    cs = utils.getCS(13,31,tree,depth,'levels','batet')
    assert math.isclose(cs,0.585,rel_tol=0.01) 

    cs = utils.getCS(30,31,tree,depth,'levels','batet')
    assert math.isclose(cs,1.585,rel_tol=0.01)

def testICs(tree):
    ic = utils.getIC(0,tree,'levels')
    assert ic == 0

    ic = utils.getIC(1,tree,'levels')
    assert ic == 1

    ic = utils.getIC(10,tree,'levels')
    assert ic == 2

    ic = utils.getIC(20,tree,'levels')
    assert ic == 3

    ic = utils.getIC(31,tree,'levels')
    assert ic == 4

        ic = utils.getIC(1,self.tree,'sanchez')
        self.assertAlmostEqual(ic,1.386,delta=0.001)

        ic = utils.getIC(10,self.tree,'sanchez')
        self.assertAlmostEqual(ic,2.128,delta=0.001)

        ic = utils.getIC(20,self.tree,'sanchez')
        self.assertAlmostEqual(ic,2.233,delta=0.001)

        ic = utils.getIC(30,self.tree,'sanchez')
        self.assertAlmostEqual(ic,2.639,delta=0.001)

def getTestTree() -> Tree:
    tree = treelib.Tree()
    tree.create_node('test', 0)

    for i in range(1,10):
        tree.create_node(i,i,parent=0)
    
    for i in range (10,14):
        tree.create_node(i,i,parent=1)

    tree.create_node(20,20,parent=10)
    tree.create_node(30,30,parent=20)
    tree.create_node(31,31,parent=20)

    # tree.create_node(40,40,parent=30)
    # tree.create_node(50,50,parent=40)
    # tree.create_node(60,60,parent=50)

    # tree.create_node(70,70,parent=60)
    # tree.create_node(71,71,parent=60)
    tree.save2file('testtree.txt')
    return tree

if __name__ == '__main__': 
    unittest.main()