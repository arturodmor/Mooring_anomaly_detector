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
            path = os.path.join(self.main_path,'txt')
            lista_archivos = os.listdir(path)

            if len(lista_archivos) == (len(df.columns) - 1):
                df.columns = ['Frequency'] + lista_archivos
            
            if mov == 'Surge':
                self.df_surge = df
            else:
                self.df_sway = df

        return self.df_surge, self.df_sway


    def plot_spectral_comparison(self,mov):
        
        figsize = (40,40)
        hspace = 0.8
        wspace = 0.2

        # Crea la figura y la cuadrícula de subplots
        plt.figure(figsize=figsize)
        gs = gridspec.GridSpec(self.n_states, self.n_dirs, width_ratios=[1, 1, 1, 1, 1])
        subplot_index = 0

        # Itera sobre cada celda de la cuadrícula de subplots y asigna los datos correspondientes
        if mov =='Surge':
            df = self.df_surge
        elif mov == 'Sway':
            df = self.df_sway

        for h in self.Hs:
            for t in self.Tp:
                for dir in self.direction:
                    filename = f'oc4__{h}__{t}__{dir}__case.txt'
                    ax = plt.subplot(gs[subplot_index])
                    ax.figure.set_size_inches(15,25)
                    if filename.replace('case', '1') in df.columns and filename.replace('case', '2') in df.columns:
                        ax.plot(df['Frequency'], df[filename.replace('case', '1')], color='b', label='Healthy')
                        ax.plot(df['Frequency'], df[filename.replace('case', '2')], color='r', label='Dragging', alpha=0.5)
                        ax.set_xlim(0, 0.15)
                        ax.set_title(f'{h}_{t}_{dir}')
                        ax.legend(['Healthy', 'Dragging'], loc='upper right', bbox_to_anchor=(0.85, 0.9))

                        subplot_index +=1

        # Ajusta el espacio entre los subplots
        plt.subplots_adjust(top=1.4,bottom=1.2, hspace=hspace, wspace=wspace)

        # Agrega un título general y una leyenda
        plt.suptitle(f'Comparativa de estados de la plataforma en {mov}',y=1,fontsize=14)
        plt.tight_layout()

        # Muestra el gráfico
        plt.show()
