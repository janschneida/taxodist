import unittest
import sys
import os
import math
import treelib
sys.path.append(os.getcwd())
from src.taxodist import td_utils as utils
  
class exceptionTests(unittest.TestCase):
    
    def setUp(self):
        self.tree = getTestTree()
        self.depth = self.tree.depth()
    
    def test_invalidCS(self):
        with self.assertRaises(SystemExit):
            utils.getCS(1,1,self.tree,self.depth,'levels','blabla')

    def test_invalidIC(self):
        with self.assertRaises(SystemExit):
            utils.getCS(1,1,self.tree,self.depth,'blabla','batet')

    def test_invalidBatet(self):
        with self.assertRaises(SystemExit):
            utils.getCS(1,1,self.tree,self.depth,'levels','batet')

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

if __name__ == '__main__': 
    unittest.main()