import sys
import os
sys.path.append(os.getcwd())
from src.taxodist import td_calc as tadi
from src.taxodist import td_utils as utils
import pandas as pd

def runParTest(code_cnt, tree):
    runtimes = []
    td = tadi.DistanceCalculations()
    for i in range(1,9):
        runtimes.append(td.calc_distance_with_codes(max_workers=i, codes=utils.getRandomCodes(code_cnt,tree), taxonomy_tree=tree))
    df_runtimes = pd.DataFrame(runtimes)
    code_cnt = str(runtimes[0][1])
    cwd = os.getcwd()
    file_name = cwd + '\\resources\\parallel_runtimes_' + str(code_cnt) + '_codes.xlsx'
    df_runtimes.to_excel(file_name)

def runSeqTest(code_cnt,tree):
    runtimes = []
    td = tadi.DistanceCalculations()
    runtimes.append(td.calc_distance_with_codes(codes=utils.getRandomCodes(code_cnt,tree),taxonomy_tree=tree, parallelized=False))
    df_runtimes = pd.DataFrame(runtimes)
    cwd = os.getcwd()
    file_name = cwd + '\\resources\\seq_runtimes.xlsx'
    df_runtimes.to_excel(file_name)

def main():
    """
    Runs performance tests with different amounts of ICD-10-GM codes and 
    different degrees of parallelization (1-8 workers) to benchmark the parallelization gain. \n

    The runtimes are saved to excel sheets for comparison.
    """
    tree = utils.getICD10GMTree()

    runParTest(100,tree)
    runParTest(2000,tree)
    runParTest(None,tree)

    runSeqTest(100,tree)
    runSeqTest(2000,tree)
    runSeqTest(None,tree)

if __name__ == "__main__":
    main()
