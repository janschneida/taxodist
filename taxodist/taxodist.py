
import pandas as pd
import icd10Utils as utils
import numpy as np
import concurrent.futures as cf
from timeit import default_timer as timer


def main(max_workers=None, code_cnt=None):
    '''Visualizes the similarity of ICD10 codes based on the ICD10 taxonomy. \n
    Saves x and y coordiantes of the codes in excel-table for further distance calculation.'''

    ######################### SETUP #########################

    tree = utils.buildICD10Tree()
    code_cnt = 1000
    # computation with all ICD codes
    ICD10_codes = utils.getAllICD10Codes(tree)
    if code_cnt:
        ICD10_codes = ICD10_codes[:code_cnt]

    # computation with 36 example codes
    # ICD10_codes = utils.getICD10CodesFromExcel()

    length = len(ICD10_codes)
    dist_matrix = np.zeros(shape=(len(ICD10_codes), len(ICD10_codes)))

    if not max_workers:
    ################## SEQUENTIAL COMPUTATION ##################
        start = timer() 
        utils.getDistMatrixSeq(ICD10_codes,tree,dist_matrix)
        time = timer() - start
        return code_cnt,time

    ################## PARALLELIZED COMPUTATION ##################

    fs = []
    with cf.ProcessPoolExecutor(max_workers=max_workers) as executor:
        max_workers = executor.__getattribute__('_max_workers')
        # print('max workers: ',max_workers)
        start = timer()
        for i in range(0,max_workers):
            # start processes and save return values 
            fs.append(executor.submit(utils.getDistMatrixWrapper, (ICD10_codes, tree, i+1, max_workers)))
    for future in cf.as_completed(fs):
        # merge partial matrices
        partial_dist_matrix, worker_index = future.result()
        dist_matrix[utils.getStart(worker_index,max_workers,length):utils.getStop(worker_index,max_workers,length)] = partial_dist_matrix
    
    dist_matrix = utils.mirrorMatrix(dist_matrix)
    time = timer() - start
 
    print('Calculation time: ', time, ' seconds')
    
    dist_matrix = utils.mirrorMatrix(dist_matrix)

    df_mds_coordinates = utils.getMDSMatrix(dist_matrix)

    # utils.saveCodeDistancesInExcel(df_mds_coordinates, ICD10_codes)

    utils.plotCodes(df_mds_coordinates, ICD10_codes)
    return max_workers, time

if __name__ == "__main__":
    main(max_workers=8)
    # runtimes = []
    # for i in range(1,9):
    #     runtimes.append(main(i,100))
    # df_runtimes = pd.DataFrame(runtimes)
    # df_runtimes.to_excel('parallel_runtimes_100_codes.xlsx')

    # for i in range(1,9):
    #     runtimes.append(main(i,2000))
    # df_runtimes = pd.DataFrame(runtimes)
    # df_runtimes.to_excel('parallel_runtimes_2000_codes.xlsx')

    # for i in range(1,9):
    #     runtimes.append(main(i))
    # df_runtimes = pd.DataFrame(runtimes)
    # df_runtimes.to_excel('parallel_runtimes_all_codes.xlsx')

    # for code_cnt in [100, 2000, None]:
    #      runtimes.append(main(code_cnt=code_cnt))
    # df_runtimes = pd.DataFrame(runtimes)
    # df_runtimes.to_excel('seq_runtimes.xlsx')
    
