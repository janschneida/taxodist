import pandas as pd 
import performance_tests as pt
import matplotlib.pyplot as plt

def main():
    # run tests to generate runtime-excel-sheets for evaluation
    pt.main()
    prepare_dataframes()
    plot_parallel_runtimes()
    plot_seq_runtimes()
    
def prepare_dataframes():
    df = pd.read_excel('seq_runtimes.xlsx',engine='openpyxl')
    df = df.drop(columns='Unnamed: 0')
    df.rename(columns={ 0 : 'Processes',1:'Runtimes'},inplace=True)
    df.iloc[26,0]=11972
    df['Processes']=df['Processes'].map(int)
    df_par_100 = df[0:8]
    df_par_100.rename(columns={'Runtimes':'Runtimes 100 codes'},inplace=True)
    df_par_2000 = df[8:16]
    df_par_2000.rename(columns={'Runtimes':'Runtimes 2000 codes'},inplace=True)
    df_par_all = df[16:24]
    df_par_all.rename(columns={'Runtimes':'Runtimes all codes'},inplace=True)
    df_seq = df[24:]
    df_seq.rename(columns={'Runtimes':'Sequential runtimes','Processes':'Code count'},inplace=True)

def plot_parallel_runtimes():
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    ax.set_yscale('log')
    ax.set_ylabel('Parallel Runtimes [s]')
    ax.set_title('Runtimes of different amounts of codes & parallelized processes')
    df_par_100.plot(0,1,ax=ax,linestyle='dotted', marker="o")
    df_par_2000.plot(0,1,ax=ax,linestyle='dotted', marker="o")
    df_par_all.plot(0,1,ax=ax,linestyle='dotted', marker="o")
    plt.savefig('parallel_runtimes.jpg')

def plot_seq_runtimes():
    fig, ax = plt.subplots()
    #fig.set_size_inches(8, 8)
    #ax.set_yscale('log')
    ax.set_ylabel('Sequential Runtimes [s]')
    ax.set_title('Sequential Runtimes of different amounts of codes')
    df_seq.plot(0,1,ax=ax, marker="o",linestyle='dotted')
    plt.savefig('seq_runtimes.jpg')

if __name__ == "__main__":
    main()