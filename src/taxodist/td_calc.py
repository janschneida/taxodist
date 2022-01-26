import sys
from treelib.tree import Tree
from src.taxodist import td_utils as utils
import numpy as np
import concurrent.futures as cf
from timeit import default_timer as timer

class DistanceCalculations:
    def __init__(self) -> None:
        pass
    def calc_distance_with_concepts(self, concepts: list=None,taxonomy_tree: Tree=None, ic_mode: str='levels', cs_mode: str='simple_wu_palmer'):
        """
        Computes the similarity of concepts based on their position in the corresponding taxonomy. \n
        Saves x and y coordiantes of the concepts in an excel-sheet for further distance calculation. \n
        Saves pairwise distances of the concepts in another excel-sheet.\n

        ----
        ## Parameters:\n
        * max_workers (int):\n
        \tThe number of parallel processes to calculate the distances. \n
        \tThis number must not be greater then the cores your system offers. \n
        \tPer default, concurrent.futures picks the "best" setting for your system.\n

        * concepts (list): \n
        \tA list of concepts to calculate the distances. \n
        \tPer default, if this parameter is left out or set to None,\n 
        \tthis method uses all concepts of the given taxonomy.\n

        * parallelized (bool):\n
        \tSets whether or not the calculation should be parallelized. \n 
        \tEspecially for smaller concept-batch-sizes it might make sense to use the serialized calculation,\n 
        \tbecause parallelization overhead might outweigh its gain. \n 
        \tPer default, the method runs in parallel.\n
        
        * taxonomy_tree (Tree):\n 
        \tA tree object representing the taxonomy you wish to calculate concept distances in. \n
        \tThis package offers methods to get trees for the following taxonomies:\n
        \t\t-ICD-10-GM (getICD10GMTree)
        \n
        * ic_mode (str):\n
        \tDefines what information-content algorithm should be used. \n
        \tThe following are available:\n
        \t\t-'levels' \n
        \t\t-'ontology' \n

        \tFor a comprehensive take on when to use which algorithm look
        \tat the README or https://doi.org/10.1186/s12911-019-0807-y
        \n
        * cs_mode (str):\n
        \tDefines what concept-similarity algorithm should be used. \n
        \tThe following are available:\n
        \t\t-'binary'  \n
        \t\t-'wu_palmer' \n
        \t\t-'li' \n
        \t\t-'simple_wu_palmer' \n

        \tFor a comprehensive take on when to use which algorithm look
        \tat the README or https://doi.org/10.1186/s12911-019-0807-y
        \n

        ----
        ## Returns:\n
        * max_workers (int):\n
        \tThe degree of parallelization.\n
        * concept_cnt (int):\n
        \tThe number of concepts for which their distances have been calculated.
        * runtime [s] (float):\n
        \tThe time in seconds it took to calculate the distances.
       
        """

        ######################### SETUP #########################
        try:
            if taxonomy_tree is None:
                raise ValueError('No taxonomy tree')
            elif taxonomy_tree.depth() == 0:
                raise ValueError('Empty taxonomy tree')
        except ValueError as err:
            print(err.args)
            sys.exit()

        if not concepts:
            concepts = utils.getAllConcepts(taxonomy_tree)

        length = len(concepts)
        dist_matrix = np.zeros(shape=(len(concepts), len(concepts)))

        fs = []
        with cf.ProcessPoolExecutor(max_workers=1) as executor:
            max_workers = executor.__getattribute__('_max_workers')
            start = timer()
            for i in range(0,max_workers):
                # start processes and save return values 
                fs.append(executor.submit(utils.getDistMatrixWrapper, (concepts, taxonomy_tree, i+1, max_workers,ic_mode,cs_mode)))
        for future in cf.as_completed(fs):
            # merge partial matrices
            partial_dist_matrix, worker_index = future.result()
            dist_matrix[utils.getStart(worker_index,max_workers,length):utils.getStop(worker_index,max_workers,length)] = partial_dist_matrix
        
        dist_matrix = utils.mirrorMatrix(dist_matrix)
        # time = timer() - start
    
        # dist_matrix = utils.mirrorMatrix(dist_matrix)

        # df_mds_coordinates = utils.getMDSMatrix(dist_matrix)

        # utils.saveconceptDistancesInExcel(df_mds_coordinates, concepts)

        return dist_matrix

    def calc_dist_for_specific_subcategory(self,concepts: list=None, taxonomy_tree: Tree=None):
        """Use this method when you know, that your concepts are from the same subcategory and that they are leaves."""
        self.calc_distance_with_concepts(concepts=concepts,taxonomy_tree=taxonomy_tree,ic_mode='levels',cs_mode='simple_wu_palmer')

    def calc_dist_for_distinct_concepts(self,concepts: list=None,taxonomy_tree: Tree=None):
        """
        Use this method when you know, that your concepts are more distinct, might not be leaves and you are working
        with a more comprehensive concept background.
        """
        self.calc_distance_with_concepts(concepts=concepts,taxonomy_tree=taxonomy_tree,ic_mode='ontology',cs_mode='wu_palmer')

