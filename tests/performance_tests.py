from numpy.lib import utils
from taxodist.taxodist import DistanceCalculations
from taxodist import taxodist_utils as utils
import pandas as pd

def main():
    """
    Runs performance tests with different amounts of codes and 
    differend degrees of parallelization to benchmark the parallelization gain. \n

    The runtimes are saved to excel sheets for comparison.
    """
    runtimes = []
    tree = utils.getICD10GMTree()
    for i in range(1,9):
        runtimes.append(DistanceCalculations.calc_distance_with_codes(max_workers=i, codes=utils.getRandomCodes(100,tree), taxonomy_tree=tree))
    df_runtimes = pd.DataFrame(runtimes)
    df_runtimes.to_excel('parallel_runtimes_100_codes.xlsx')

    runtimes = []
    for i in range(1,9):
        runtimes.append(DistanceCalculations.calc_distance_with_codes(max_workers=i, codes=utils.getRandomCodes(2000,tree), taxonomy_tree=tree))
    df_runtimes = pd.DataFrame(runtimes)
    df_runtimes.to_excel('parallel_runtimes_2000_codes.xlsx')

    runtimes = []
    for i in range(1,9):
        runtimes.append(DistanceCalculations.calc_distance_with_codes(max_workers=i,taxonomy_tree=tree))
    df_runtimes = pd.DataFrame(runtimes)
    df_runtimes.to_excel('parallel_runtimes_all_codes.xlsx')

    runtimes = []
    for code_cnt in [100, 2000, None]:
         runtimes.append(DistanceCalculations.calc_distance_with_codes(code_cnt=code_cnt))
    df_runtimes = pd.DataFrame(runtimes)
    df_runtimes.to_excel('seq_runtimes.xlsx')

if __name__ == "__main__":
    main()