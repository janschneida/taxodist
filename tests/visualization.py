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
    # set up data to get list of patient diagnoses-sets
    df_moltb = pd.read_excel("pseudo_icd10_moltb.xlsx")
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
    plt.savefig('plots.svg',format='svg')
    

if __name__ == '__main__': 
    main()