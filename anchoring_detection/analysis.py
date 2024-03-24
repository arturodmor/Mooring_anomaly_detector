from anchoring_detection.preprocess import Preprocess
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from fatiguepy import *
import os
import pandas as pd

class Analysis(Preprocess):
    def __init__(self, dataframes_surge=None, dataframes_sway=None, df_surge = None, df_sway = None, n_states=10, n_dirs=5):
        super().__init__(movements=['Surge', 'Sway'], main_path=rf'D:\arturo_sim\simulaciones\acoplado', dataframes_surge=dataframes_surge, dataframes_sway=dataframes_sway)
        self.df_surge = df_surge
        self.df_sway = df_sway
        self.n_states = n_states
        self.n_dirs =n_dirs
    

    def dataframe_for_analysis(self):

        for mov in self.movements:
            if mov == 'Surge':
                dataframes = self.dataframes_surge
            else:
                dataframes = self.dataframes_sway

            # Group the data in one unique dataframe
            df= pd.concat(dataframes.values(), axis=1)
            df_freq = df.iloc[:,0]
            df = df.drop(df.filter(like='Frequencies').columns, axis=1)
            df.insert(0,'Frequency',df_freq)

            # the number of txt files is the same of dataframe amplitude columns. We are going to regroup with only one "freq_colum" because it is the same
            path = os.path.join(self.main_path,'pruebas_txt')
            lista_archivos = os.listdir(path)

            if len(lista_archivos) == (len(df.columns) - 1):
                df.columns = ['Frequency'] + lista_archivos
            
            if mov == 'Surge':
                self.df_surge = df
            else:
                self.df_sway = df

        return self.df_surge, self.df_sway


    def plot_spectral_comparison(self):
        pass