from numpy.lib import utils
import taxodist.taxodist as td
import taxodist.taxodist_utils as utils
import pandas as pd


def main():
    '''
    Runs performance tests with different amounts of codes and 
    differend degrees of parallelization to benchmark the parallelization gain. \n

    The runtimes are saved to excel sheets for comparison.
    '''
    runtimes = []
    for i in range(1,9):
        runtimes.append(td.DistanceCalculations.calc_distance_with_codes(i,100))
    df_runtimes = pd.DataFrame(runtimes)
    df_runtimes.to_excel('parallel_runtimes_100_codes.xlsx')

    runtimes = []
    for i in range(1,9):
        runtimes.append(td.DistanceCalculations.calc_distance_with_codes(i,2000))
    df_runtimes = pd.DataFrame(runtimes)
    df_runtimes.to_excel('parallel_runtimes_2000_codes.xlsx')

    runtimes = []
    for i in range(1,9):
        runtimes.append(td.DistanceCalculations.calc_distance_with_codes(i))
    df_runtimes = pd.DataFrame(runtimes)
    df_runtimes.to_excel('parallel_runtimes_all_codes.xlsx')

    runtimes = []
    for code_cnt in [100, 2000, None]:
         runtimes.append(td.DistanceCalculations.calc_distance_with_codes(code_cnt=code_cnt))
    df_runtimes = pd.DataFrame(runtimes)
    df_runtimes.to_excel('seq_runtimes.xlsx')

def get_random_codes(code_cnt: int) -> list:
    '''
    Returns list with code_cnt random codes.
    '''
    utils.

if __name__ == "__main__":
    main()