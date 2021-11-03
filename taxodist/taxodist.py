import taxodist_utils as utils
import numpy as np
import concurrent.futures as cf
from timeit import default_timer as timer

class DistanceCalculations:
    def calc_distance_with_codes(max_workers=None,codes=None,parallelized=True,plot_when_finished=False,taxonomy='icd10gm'):
        '''
        Visualizes the similarity of ICD10 codes based on the ICD10 taxonomy. \n
        Saves x and y coordiantes of the codes in an excel-sheet for further distance calculation. \n
        Saves pairwise distances of the codes in another excel-sheet.\n

            Parameters:
                max_workers (int): 
                                The number of parallel processes to calculate the distances. \n
                                This number must not be greater then the cores your system offers. \n
                                Per default, concurrent.futures picks the "best" setting for your system.
                codes (list): 
                                A list of ICD-10 codes to calculate the distances based on their position in the ICD-10-GM hierarchy. \n
                                Per default, this method calculates a complete list of all available ICD-10-GM codes.
                parallelized (bool):
                                Sets whether or not the calculation should be parallelized. \n 
                                Especially for smaller code-batch-sizes it might make sense to use the serialized calculation, 
                                because parallelization overhead might outweigh its gain. \n 
                                Per default, the method runs in parallel.
                plot_when_finished (bool):
                                Sets whether or not to plot the relative distances of the codes after the calculation.

            Returns:
                max_workers (int):
                                The degree of parallelization.
                code_cnt (int):
                                The number of codes for which their distances have been calculated.
                runtime [s] (float):
                                The time in seconds it took to calculate the distances.
        '''

        ######################### SETUP #########################

        tree = utils.buildICD10Tree() #TODO add function for tree generation as parameter from outside
        ICD10_codes = codes
        if not ICD10_codes:
            ICD10_codes = utils.getAllICD10Codes(tree)

        length = len(ICD10_codes)
        dist_matrix = np.zeros(shape=(len(ICD10_codes), len(ICD10_codes)))

        if not parallelized:
        ################## SEQUENTIAL COMPUTATION ##################
            start = timer() 
            utils.getDistMatrixSeq(ICD10_codes,tree,dist_matrix)
            time = timer() - start
            return 0,length,time

        ################## PARALLELIZED COMPUTATION ##################

        fs = []
        with cf.ProcessPoolExecutor(max_workers=max_workers) as executor:
            max_workers = executor.__getattribute__('_max_workers')
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
    
        # print('Calculation time: ', time, ' seconds')
        
        dist_matrix = utils.mirrorMatrix(dist_matrix)

        df_mds_coordinates = utils.getMDSMatrix(dist_matrix)

        utils.saveCodeDistancesInExcel(df_mds_coordinates, ICD10_codes)

        if plot_when_finished:
            utils.plotCodes(df_mds_coordinates, ICD10_codes)
        return max_workers,length,time

        
