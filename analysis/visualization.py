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
#plt.style.use("seaborn")

def main():
    #allMOLTBPats()
    pancreasPatients()
    return
    

def allMOLTBPats():
    # set up data to get list of patient diagnoses-sets
    df_moltb = pd.read_excel('resources/pseudo_icd10_moltb.xlsx')
    patient_icd = df_moltb.groupby(df_moltb.PseudoPatNr.name)['ICD'].agg(list).reset_index(name='ICD')
    patient_icd_array = patient_icd.to_numpy()
    moltb_icd_sets = [set(icd_list) for patient, icd_list in patient_icd_array]
    setnames = ['patient ' + str(x) for x in range(1,len(moltb_icd_sets))]
    
    tree = tree_parsers.getICD10GMTree(version='2021')
    td = td_calc.Taxodist()
    # use taxodist to calculate similarity of all patients
    dist_matrix = td.calc_set_sim(moltb_icd_sets,tree,'levels','nguyen_almubaid','bipartite_matching',normalize=False)

    df_mds_coordinates = utils.getMDSMatrix(dist_matrix)
    # plotting/saving figure as svg
    fig, ax = plt.subplots()
    df_mds_coordinates.plot(0, 1, kind='scatter', ax=ax)

    for k, v in df_mds_coordinates.iterrows():
        ax.annotate(setnames[k], v)
    plt.savefig('all_mtb_pats_L_NA_BIP.svg',format='svg')

def pancreasPatients():
    #retrieve patients with pancreas neoplasm (C25) as main diagnoses
    df_hd_moltb = pd.read_excel('analysis/resources/pseudo_icd10_hauptdiagnose_moltb.xlsx')
    df_pancreas_hd = df_hd_moltb[df_hd_moltb['ICD-10 Hauptdiagnose'].str.contains('C25')]

    df_moltb = pd.read_excel('analysis/resources/pseudo_icd10_moltb.xlsx')
    df_patient_icd = df_moltb.groupby(df_moltb.PseudoPatNr.name)['ICD'].agg(list).reset_index(name='ICD')
    df_pancreas_patient = df_patient_icd[df_patient_icd['PseudoPatNr'].isin(df_pancreas_hd['Pseudonym'])]
    
    pancreas_patient_array = df_pancreas_patient.to_numpy()
    pancreas_icd_sets = [set(icd_list) for patient, icd_list in pancreas_patient_array]
    # setnames = [str(pseudonym) for pseudonym, icd in pancreas_patient_array]
    setnames = ['patient ' + str(i) for i, icd in enumerate(pancreas_patient_array)]

    tree = tree_parsers.getICD10GMTree(version='2021')
    td = td_calc.Taxodist()
    # use taxodist to calculate similarity of all patients
    dist_matrix = td.calc_set_sim(pancreas_icd_sets,tree,'levels','nguyen_almubaid','bipartite_matching',normalize=False)
    
    pd.DataFrame(dist_matrix).to_excel('pancreas_pats_dist_L_NA_BIP.xlsx')
    
    df_mds_coordinates = utils.getMDSMatrix(dist_matrix)
    
    # plotting/saving figure as svg
    fig, ax = plt.subplots()
    df_mds_coordinates.plot(0, 1, kind='scatter', ax=ax)
    for k, v in df_mds_coordinates.iterrows():
        ax.annotate(setnames[k], v)
    plt.savefig('panceas_pats_numbered_pats.svg',format='svg')
    plt.show()
    # utils.plotDistMatrix(df_mds_coordinates,setnames)

if __name__ == '__main__': 
    main()