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
    #pancreasPatients()
    runAllSetSims()
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
    
    # pd.DataFrame(dist_matrix).to_excel('pancreas_pats_dist_L_NA_BIP.xlsx')
    
    # df_mds_coordinates = utils.getMDSMatrix(dist_matrix)
    
    # # plotting/saving figure as svg
    # fig, ax = plt.subplots()
    # df_mds_coordinates.plot(0, 1, kind='scatter', ax=ax)
    # for k, v in df_mds_coordinates.iterrows():
    #     ax.annotate(setnames[k], v)
    # plt.savefig('panceas_pats_numbered_pats.svg',format='svg')
    # plt.show()
    # # utils.plotDistMatrix(df_mds_coordinates,setnames)

def pancreasPatientsExpertValues() -> np.ndarray:
    ''' Retrieve & plot expert's similarities '''
    
    df = pd.read_excel('analysis\local\\resources\pankreas_patienten_matrix_MB.xlsx')
    df = df.drop(axis=1,columns='Unnamed: 0')
    df = df.set_index(df.columns)
    df[df.isna()] = 0.0

    matrix = utils.mirrorMatrix(df.to_numpy())
    # df_mds_dist = utils.getMDSMatrix(matrix)
    # utils.plotDistMatrix(df_mds_dist,df.columns)
    return matrix
    
def runAllSetSims():
    # TODO normalized correlations + sim/dist mixes
    ics = ['levels','sanchez']
    
    c_dists = ['nguyen_almubaid','path_based']
    setdists = ['bipartite_matching','hierarchical']
    
    c_sims = ['leacock_chodorow','simple_wu_palmer','li','wu_palmer'] # 'batet', TODO talk about batet -> cant compare same concepts
    setsims = ['mean_cs','bipartite_matching'] 
    setsims_triv = ['overlap','cosine','dice','jaccard']  
    
    expert_sim_matrix = pancreasPatientsExpertValues()
    expert_dist_matrix = 1 - expert_sim_matrix/10
    
    #retrieve patients with pancreas neoplasm (C25) as main diagnoses
    df_hd_moltb = pd.read_excel('analysis/resources/pseudo_icd10_hauptdiagnose_moltb.xlsx')
    df_pancreas_hd = df_hd_moltb[df_hd_moltb['ICD-10 Hauptdiagnose'].str.contains('C25')]

    df_moltb = pd.read_excel('analysis/resources/pseudo_icd10_moltb.xlsx')
    df_patient_icd = df_moltb.groupby(df_moltb.PseudoPatNr.name)['ICD'].agg(list).reset_index(name='ICD')
    df_pancreas_patient = df_patient_icd[df_patient_icd['PseudoPatNr'].isin(df_pancreas_hd['Pseudonym'])]
    
    pancreas_patient_array = df_pancreas_patient.to_numpy()
    pancreas_icd_sets = [set(icd_list) for patient, icd_list in pancreas_patient_array]
    # setnames = [str(pseudonym) for pseudonym, icd in pancreas_patient_array]
    # setnames = ['patient ' + str(i) for i, icd in enumerate(pancreas_patient_array)]

    tree = tree_parsers.getICD10GMTree(version='2021')
    td = td_calc.Taxodist()
    
    # # similarity calculations with "trivial" setsims UNSCALED
    # for setsim in setsims_triv:
    #     # use taxodist to calculate similarity of all patient sets
    #     td_matrix = td.calc_set_sim(pancreas_icd_sets,tree,ic_mode='',cs_mode='',setsim_mode=setsim,normalize=False,scale_to_setsizes=False)
    #     # mds_matrix = utils.getMDSMatrix(td_matrix)
    #     correlation = np.corrcoef(expert_sim_matrix.flatten(),td_matrix.flatten())
    #     combination = setsim+'_unscaled'
    #     print('combination: ',combination,'\ncorrelation: ',correlation)
    #     pd.DataFrame(td_matrix).to_excel(combination+'_matrix.xlsx')
    #     pd.DataFrame(correlation).to_excel(combination+'_correlation.xlsx') 
        
    # # similarity calculations with "trivial" setsims SCALED
    # for setsim in setsims_triv:
    #     # use taxodist to calculate similarity of all patient sets
    #     td_matrix = td.calc_set_sim(pancreas_icd_sets,tree,ic_mode='',cs_mode='',setsim_mode=setsim,normalize=False,scale_to_setsizes=True)
    #     # mds_matrix = utils.getMDSMatrix(td_matrix)
    #     correlation = np.corrcoef(expert_sim_matrix.flatten(),td_matrix.flatten())
    #     combination = setsim+'_scaled'
    #     print('combination: ',combination,'\ncorrelation: ',correlation)
    #     pd.DataFrame(td_matrix).to_excel(combination+'_matrix.xlsx')
    #     pd.DataFrame(correlation).to_excel(combination+'_correlation.xlsx')                 
    
    # distance correlations SCALED
    for ic in ics:
        for cd in c_dists:
            for sd in setdists:
                combination = ic+'_'+cd+'_'+sd+'_scaled'
                # use taxodist to calculate similarity of all patient sets
                td_matrix = td.calc_set_sim(pancreas_icd_sets,tree,ic,cd,sd,normalize=False,scale_to_setsizes=True)
                # mds_matrix = utils.getMDSMatrix(td_matrix)
                correlation = np.corrcoef(expert_dist_matrix.flatten(),td_matrix.flatten())
                print('combination: ',combination,'\ncorrelation: ',correlation)  
                pd.DataFrame(td_matrix).to_excel(combination+'_matrix.xlsx')
                pd.DataFrame(correlation).to_excel(combination+'_correlation.xlsx')
                
    # distance correlations UNSCALED
    for ic in ics:
        for cd in c_dists:
            for sd in setdists:
                combination = ic+'_'+cd+'_'+sd+'_unscaled'
                # use taxodist to calculate similarity of all patient sets
                td_matrix = td.calc_set_sim(pancreas_icd_sets,tree,ic,cd,sd,normalize=False,scale_to_setsizes=False)
                # mds_matrix = utils.getMDSMatrix(td_matrix)
                correlation = np.corrcoef(expert_dist_matrix.flatten(),td_matrix.flatten())
                print('combination: ',combination,'\ncorrelation: ',correlation)  
                pd.DataFrame(td_matrix).to_excel(combination+'_matrix.xlsx')
                pd.DataFrame(correlation).to_excel(combination+'_correlation.xlsx')
                
    # similarity correlations SCALED        
    for ic in ics:
        for cs in c_sims:
            for setsim in setsims:
                # use taxodist to calculate similarity of all patient sets
                td_matrix = td.calc_set_sim(pancreas_icd_sets,tree,ic,cs,setsim,normalize=False,scale_to_setsizes=True)
                # mds_matrix = utils.getMDSMatrix(td_matrix)
                correlation = np.corrcoef(expert_sim_matrix.flatten(),td_matrix.flatten())
                combination = ic+'_'+cs+'_'+setsim+'_scaled'
                print('combination: ',combination,'\ncorrelation: ',correlation)
                pd.DataFrame(td_matrix).to_excel(combination+'_matrix.xlsx')
                pd.DataFrame(correlation).to_excel(combination+'_correlation.xlsx') 
                
    # similarity correlations UNSCALED        
    for ic in ics:           
        for cs in c_sims:
            for setsim in setsims:
                # use taxodist to calculate similarity of all patient sets
                td_matrix = td.calc_set_sim(pancreas_icd_sets,tree,ic,cs,setsim,normalize=False,scale_to_setsizes=False)
                # mds_matrix = utils.getMDSMatrix(td_matrix)
                correlation = np.corrcoef(expert_sim_matrix.flatten(),td_matrix.flatten())
                combination = ic+'_'+cs+'_'+setsim+'_unscaled'
                print('combination: ',combination,'\ncorrelation: ',correlation)
                pd.DataFrame(td_matrix).to_excel(combination+'_matrix.xlsx')
                pd.DataFrame(correlation).to_excel(combination+'_correlation.xlsx')           
                 

if __name__ == '__main__': 
    main()