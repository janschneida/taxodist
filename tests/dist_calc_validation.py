import sys
import os
import math
import treelib
sys.path.append(os.getcwd())
from src.taxodist import td_calc as td
from src.taxodist import td_utils as utils

def main():
    """
    Runs tests with different codes to validate the implemented algorithms.\n

    The ground-truth is derived by manually calculating the values for the respective codes.
    """
    tree = getTestTree()
    depth = tree.depth

    cs = utils.getCS('','',tree,depth)
    assert cs == 0.5

    cs = utils.getCS('','',tree,depth)
    assert cs == 0.5

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