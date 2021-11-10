import sys
import os
sys.path.append(os.getcwd())
from src.taxodist import td_calc as td
from src.taxodist import td_utils as utils

def main():
    """
    Runs tests with different codes to valiate the pairwise distance calculations.\n

    The ground-truth is derived by manually calculating the values for the respective codes.
    """
    tree = utils.getICD10GMTree()
    depth = tree.depth

    cs = utils.getCS('','',tree,depth)
    assert cs == 0.5

    cs = utils.getCS('','',tree,depth)
    assert cs == 0.5

    cs = utils.getCS('','',tree,depth)
    assert cs == 0.5

    cs = utils.getCS('','',tree,depth)
    assert cs == 0.5

    cs = utils.getCS('','',tree,depth)
    assert cs == 0.5

    cs = utils.getCS('','',tree,depth)
    assert cs == 0.5

    cs = utils.getCS('','',tree,depth)
    assert cs == 0.5

if __name__ == "__main__":
    main()