import sys
import os
sys.path.append(os.getcwd())
from src.taxodist import td_utils as utils
from src.taxodist import tree_parsers
from src.taxodist import td_calc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pylab as plt
import seaborn as sn

def getPancreasPatientsExpertValues() -> np.ndarray:
    ''' Retrieve & plot expert's similarities '''
    
    df = pd.read_excel('analysis\local\\resources\pankreas_patienten_matrix_MB.xlsx')
    df = df.drop(axis=1,columns='Unnamed: 0')
    df = df.set_index(df.columns)
    df[df.isna()] = 0.0

    matrix = utils.mirrorMatrix(df.to_numpy())
    # df_mds_dist = utils.getMDSMatrix(matrix)
    # utils.plotDistMatrix(df_mds_dist,df.columns)
    return matrix

def getPancreasICDSets() -> list:
    ''' get lists of ICD codes of all patients with C25.X maindiagnoses'''
    
    df_hd_moltb = pd.read_excel('analysis/resources/pseudo_icd10_hauptdiagnose_moltb.xlsx')
    df_pancreas_hd = df_hd_moltb[df_hd_moltb['ICD-10 Hauptdiagnose'].str.contains('C25')]

    df_moltb = pd.read_excel('analysis/resources/pseudo_icd10_moltb.xlsx')
    df_patient_icd = df_moltb.groupby(df_moltb.PseudoPatNr.name)['ICD'].agg(list).reset_index(name='ICD')
    df_pancreas_patient = df_patient_icd[df_patient_icd['PseudoPatNr'].isin(df_pancreas_hd['Pseudonym'])]
    
    pancreas_patient_array = df_pancreas_patient.to_numpy()
    return [set(icd_list) for patient, icd_list in pancreas_patient_array]

def getCorrelationDict() -> dict:
    dir = 'analysis/generated/correlations_AND_dist_sim_matrices'
    correlation_dict = {}
    for file in os.listdir(dir):
        if 'correlation' in file:
            df = pd.read_excel(dir+'/'+file)
            corr = df[0][1]
            combination = file.replace('_correlation.xlsx','')
            correlation_dict[combination] = abs(corr)
    return correlation_dict

def sortSimMatrixByICDSetSize(matrix) -> list:
    ''' sorts given similarity matrix by the number diagnoses per patient (setsize)'''
    icd_sets = getPancreasICDSets()
    set_len = []
    for patientset in icd_sets:
        set_len.append(len(patientset))

    len_sort_indices = np.argsort(set_len)
    # sort rows
    matrix = [matrix[i] for i in len_sort_indices]
    #sort columns
    for i, patient_sim_vector in enumerate(matrix):
        matrix[i] = [patient_sim_vector[j] for j in len_sort_indices]
    return matrix

