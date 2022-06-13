import sys
from treelib.tree import Tree
from src.taxodist import td_utils as utils
import numpy as np
import concurrent.futures as cf
from timeit import default_timer as timer
from sklearn import preprocessing

class Taxodist:
    def __init__(self) -> None:
        pass
    def calc_distance_with_concepts(self, concepts: list=None,taxonomy_tree: Tree=None, ic_mode: str='levels', cs_mode: str='simple_wu_palmer', normalize: bool= False, calc_mode: str='distance'):
        """
        Computes the distance or similarity of concepts based on their position in the corresponding taxonomy. \n
        Saves x and y coordiantes of the concepts in an excel-sheet for further distance calculation. \n
        Saves pairwise distances of the concepts in another excel-sheet.\n

        ----
        ## Parameters:\n

        * concepts (list): \n
        \tA list of concepts to calculate the distances. \n
        \tPer default, if this parameter is left out or set to None,\n 
        \tthis method uses all concepts of the given taxonomy.\n
        
        * taxonomy_tree (Tree):\n 
        \tA tree object representing the taxonomy you wish to calculate concept distances in. \n
        \tThis package offers methods to get trees for the following taxonomies:\n
        \t\t-ICD-10-GM (getICD10GMTree)
        \n
        * ic_mode (str):\n
        \tDefines what information-content algorithm should be used. \n
        \tThe following are available:\n
        \t\t-'levels' \n
        \t\t-'sanchez' \n

        * cs_mode (str):\n
        \tDefines what concept-similarity algorithm should be used. \n
        \tThe following are available:\n
        \t\t-'wu_palmer' \n
        \t\t-'li' \n
        \t\t-'simple_wu_palmer' \n
        \t\t-'leacock_chodorow' \n
        \t\t-'nguyen_almubaid' \n
        \t\t-'batet' \n
       
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
        #TODO not dist matrix, but sim matrix -> normalize & substract from 1 to get distances
        dist_matrix = np.zeros(shape=(len(concepts), len(concepts)))

        fs = []
        with cf.ProcessPoolExecutor(max_workers=1) as executor:
            max_workers = executor.__getattribute__('_max_workers')
            for i in range(0,max_workers):
                # start processes and save return values 
                fs.append(executor.submit(utils.getDistMatrixWrapper, (concepts, taxonomy_tree, i+1, max_workers,ic_mode,cs_mode)))
        for future in cf.as_completed(fs):
            # merge partial matrices
            partial_dist_matrix, worker_index = future.result()
            dist_matrix[utils.getStart(worker_index,max_workers,length):utils.getStop(worker_index,max_workers,length)] = partial_dist_matrix
        
        dist_matrix = utils.mirrorMatrix(dist_matrix)

        if normalize:
            scaler = preprocessing.MinMaxScaler()
            dist_matrix = scaler.fit_transform(dist_matrix)

        # if calc_mode == 'distance':
        #     if cs_mode == ''

        df_mds_coordinates = utils.getMDSMatrix(dist_matrix)

        utils.saveConceptDistancesInExcel(df_mds_coordinates, concepts)

        return dist_matrix

    def calc_dist_for_specific_subcategory(self,concepts: list=None, taxonomy_tree: Tree=None):
        """Use this method when you know, that your concepts are from the same subcategory and that they are leaves."""
        self.calc_distance_with_concepts(concepts=concepts,taxonomy_tree=taxonomy_tree,ic_mode='levels',cs_mode='simple_wu_palmer')

    def calc_dist_for_distinct_concepts(self,concepts: list=None,taxonomy_tree: Tree=None):
        """
        Use this method when you know, that your concepts are more distinct, might not be leaves and you are working
        with a more comprehensive concept background.
        """
        self.calc_distance_with_concepts(concepts=concepts,taxonomy_tree=taxonomy_tree,ic_mode='sanchez',cs_mode='wu_palmer')

