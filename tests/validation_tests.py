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
    def setUp(self):
        self.tree = getTestTree()
        self.depth = self.tree.depth()

    # def test_SetSims(self,tree, depth):
    #     return

    def test_CSs(self):
        # WU PALMER TESTS

        cs = utils.getCS(1,1,self.tree,self.depth,'level','wu_palmer')
        self.assertEqual(cs,1.0)

        cs = utils.getCS(1,9,self.tree,self.depth,'level','wu_palmer')
        self.assertEqual(cs,0.0)

        cs = utils.getCS(13,31,self.tree,self.depth,'level','wu_palmer')
        self.assertAlmostEqual(cs,0.333,delta=0.001)

        cs = utils.getCS(30,31,self.tree,self.depth,'level','wu_palmer')
        self.assertEqual(cs,0.75)

        # LI TESTS

        cs = utils.getCS(1,1,self.tree,self.depth,'level','li')
        self.assertEqual(cs,0.0)

        cs = utils.getCS(31,31,self.tree,self.depth,'level','li')
        self.assertAlmostEqual(cs,1.412,delta=0.001)

        cs = utils.getCS(1,9,self.tree,self.depth,'level','li')
        self.assertEqual(cs,0.0)

        cs = utils.getCS(13,31,self.tree,self.depth,'level','li')
        self.assertAlmostEqual(cs,1.195,delta=0.001)

        cs = utils.getCS(30,31,self.tree,self.depth,'level','li')
        self.assertAlmostEqual(cs,1.412,delta=0.001)

        # cs = utils.getCS(70,71,self.tree,self.depth,'level','li')
        # assert math.isclose(cs,1.491,rel_tol=0.01)

        # cs = utils.getCS(71,71,self.tree,self.depth,'level','li')
        # assert math.isclose(cs,1.491,rel_tol=0.01)

        # SIMPLE WU PALMER TESTS

        cs = utils.getCS(1,1,self.tree,self.depth,'level','simple_wu_palmer')
        self.assertEqual(cs,1.0)

        cs = utils.getCS(1,9,self.tree,self.depth,'level','simple_wu_palmer')
        self.assertEqual(cs,0.0)

        cs = utils.getCS(13,31,self.tree,self.depth,'level','simple_wu_palmer')
        self.assertAlmostEqual(cs,0.25,delta=0.01)

        cs = utils.getCS(30,31,self.tree,self.depth,'level','simple_wu_palmer')
        self.assertEqual(cs,0.75)

        # LEACOCK CHODOROW TESTS

        cs = utils.getCS(1,1,self.tree,self.depth,'level','leacock_chodorow')
        self.assertAlmostEqual(cs,0.980,delta=0.001)

        cs = utils.getCS(1,9,self.tree,self.depth,'level','leacock_chodorow')
        self.assertAlmostEqual(cs,0.980,delta=0.001)

        cs = utils.getCS(13,31,self.tree,self.depth,'level','leacock_chodorow')
        self.assertAlmostEqual(cs,0.470,delta=0.001)

        cs = utils.getCS(30,31,self.tree,self.depth,'level','leacock_chodorow')
        self.assertAlmostEqual(cs,0.980,delta=0.001)

        # NGUYEN AL-MUBAID TESTS

        cs = utils.getCS(1,1,self.tree,self.depth,'level','nguyen_almubaid')
        self.assertAlmostEqual(cs,1.609,delta=0.001)

        cs = utils.getCS(1,9,self.tree,self.depth,'level','nguyen_almubaid')
        self.assertAlmostEqual(cs,1.609,delta=0.001)

        cs = utils.getCS(13,31,self.tree,self.depth,'level','nguyen_almubaid')
        self.assertAlmostEqual(cs,2.303,delta=0.001)

        cs = utils.getCS(30,31,self.tree,self.depth,'level','nguyen_almubaid')
        self.assertAlmostEqual(cs,0.693,delta=0.001)

    # BATET TESTS

    cs = utils.getCS(1,1,tree,depth,'level','nguyen_almubaid')
    assert math.isclose(cs,1.609,rel_tol=0.01)

    cs = utils.getCS(1,9,tree,depth,'level','nguyen_almubaid')
    assert math.isclose(cs,1.609,rel_tol=0.01)

    cs = utils.getCS(13,31,tree,depth,'level','nguyen_almubaid')
    assert math.isclose(cs,2.303,rel_tol=0.01)

    cs = utils.getCS(30,31,tree,depth,'level','nguyen_almubaid')
    assert math.isclose(cs,0.693,rel_tol=0.01)



    def test_ICs(self):
        ic = utils.getIC(0,self.tree,'level')
        self.assertEqual(ic,0)

        ic = utils.getIC(1,self.tree,'level')
        self.assertEqual(ic,1)

        ic = utils.getIC(10,self.tree,'level')
        self.assertEqual(ic,2)

        ic = utils.getIC(20,self.tree,'level')
        self.assertEqual(ic,3)

        ic = utils.getIC(31,self.tree,'level')
        self.assertEqual(ic,4)

        ic = utils.getIC(0,self.tree,'sanchez')
        self.assertEqual(ic,0.0)

        ic = utils.getIC(1,self.tree,'sanchez')
        self.assertAlmostEqual(ic,1.386,delta=0.001)

        ic = utils.getIC(10,self.tree,'sanchez')
        self.assertAlmostEqual(ic,2.128,delta=0.001)

        ic = utils.getIC(20,self.tree,'sanchez')
        self.assertAlmostEqual(ic,2.233,delta=0.001)

        ic = utils.getIC(30,self.tree,'sanchez')
        self.assertAlmostEqual(ic,2.639,delta=0.001)

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

    # tree.create_node(40,40,parent=30)
    # tree.create_node(50,50,parent=40)
    # tree.create_node(60,60,parent=50)

    # tree.create_node(70,70,parent=60)
    # tree.create_node(71,71,parent=60)
    tree.save2file('testtree.txt')
    return tree

if __name__ == '__main__': 
    unittest.main()