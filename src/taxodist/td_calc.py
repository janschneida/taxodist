import td_utils as utils
import numpy as np
import concurrent.futures as cf
from timeit import default_timer as timer

class DistanceCalculations:
    def calc_distance_with_codes(max_workers: int = None,codes=None,parallelized=True,plot_when_finished=False,taxonomy_tree=None):
        """
        Computes the similarity of codes based on their position in the corresponding taxonomy. \n
        Saves x and y coordiantes of the codes in an excel-sheet for further distance calculation. \n
        Saves pairwise distances of the codes in another excel-sheet.\n

            Parameters:
                max_workers (int): 
                                The number of parallel processes to calculate the distances. \n
                                This number must not be greater then the cores your system offers. \n
                                Per default, concurrent.futures picks the "best" setting for your system.
                codes (list): 
                                A list of codes to calculate the distances. \n
                                Per default, if this parameter is left out or set to None, this method uses all codes of the given taxonomy.
                parallelized (bool):
                                Sets whether or not the calculation should be parallelized. \n 
                                Especially for smaller code-batch-sizes it might make sense to use the serialized calculation, 
                                because parallelization overhead might outweigh its gain. \n 
                                Per default, the method runs in parallel.
                plot_when_finished (bool):
                                Sets whether or not to plot the relative distances of the codes after the calculation.
                taxonomy_tree (Tree): 
                                A tree object representing the taxonomy you wish to calculate code distances in. \n
                                This package offers methods to get trees for the following taxonomies:
                                    - ICD-10-GM (getICD10GMTree)

            Returns:
                max_workers (int):
                                The degree of parallelization.
                code_cnt (int):
                                The number of codes for which their distances have been calculated.
                runtime [s] (float):
                                The time in seconds it took to calculate the distances.
        """

        ######################### SETUP #########################

        if not codes:
            codes = utils.getAllCodes(taxonomy_tree)

        length = len(codes)
        dist_matrix = np.zeros(shape=(len(codes), len(codes)))

        if not parallelized:
        ################## SEQUENTIAL COMPUTATION ##################
            start = timer() 
            utils.getDistMatrixSeq(codes,taxonomy_tree,dist_matrix)
            time = timer() - start
            return 0,length,time

        ################## PARALLELIZED COMPUTATION ##################

        fs = []
        with cf.ProcessPoolExecutor(max_workers=max_workers) as executor:
            max_workers = executor.__getattribute__('_max_workers')
            start = timer()
            for i in range(0,max_workers):
                # start processes and save return values 
                fs.append(executor.submit(utils.getDistMatrixWrapper, (codes, taxonomy_tree, i+1, max_workers)))
        for future in cf.as_completed(fs):
            # merge partial matrices
            partial_dist_matrix, worker_index = future.result()
            dist_matrix[utils.getStart(worker_index,max_workers,length):utils.getStop(worker_index,max_workers,length)] = partial_dist_matrix
        
        dist_matrix = utils.mirrorMatrix(dist_matrix)
        time = timer() - start
    
        # print('Calculation time: ', time, ' seconds')
        
        # dist_matrix = utils.mirrorMatrix(dist_matrix)

        # df_mds_coordinates = utils.getMDSMatrix(dist_matrix)

        # utils.saveCodeDistancesInExcel(df_mds_coordinates, codes)

        # if plot_when_finished:
        #     utils.plotCodes(df_mds_coordinates, codes)
        return max_workers,length,time

        
