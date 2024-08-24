from anchoring_detection.preprocess import Preprocess
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from fatiguepy import *
import os
import pandas as pd

class Analysis(Preprocess):

    "Class to explore data behavior and representation clue information"

    def __init__(self, df_surge = None, df_sway = None, n_states=10, n_dirs=5):
        super().__init__()
        self.df_surge = df_surge
        self.df_sway = df_sway
        self.n_states = n_states
        self.n_dirs =n_dirs
    

    def dataframe_for_analysis(self,domain = 'Time'):
        """To group all spectra movements in a unique dataframe

        Args:
            domain(str): To stablish the study domain of the dataset ('Time' or 'Frequency')

        Returns:
            Surge and Sway Dataframes with all spectra
        """

        for mov in self.movements:
            if mov == 'Surge':
                dataframes = self.dataframes_surge
            else:
                dataframes = self.dataframes_sway

            # Group the data in one unique dataframe
            df= pd.concat(dataframes.values(), axis=1)
            df_domain = df.iloc[:,0]

            if domain == 'Time':
                df = df.drop(df.filter(like='time[s]').columns, axis=1)
            elif domain == 'Frequency':
                df = df.drop(df.filter(like='Frequencies').columns, axis=1)

            df.insert(0,domain,df_domain)

            # the number of txt files is the same of dataframe amplitude columns. We are going to regroup with only one "time/frequency colum" because it is the same
            file_list = sorted(os.listdir(self.main_path))

            if len(file_list) == (len(df.columns) - 1):
                df.columns = [domain] + file_list

            if mov == 'Surge':
                self.df_surge = df
                #self.df_surge.to_pickle(os.path.join(self.base_dir,'..','data','df_surge.pkl'))
            else:
                self.df_sway = df
                #self.df_surge.to_pickle(os.path.join(self.base_dir,'..','data','df_sway.pkl'))



    def plot_spectral_comparison(self,mov,domain = 'Time'):
        """To represent spectral comparison with for all sea states

        Args:
            domain(str): To stablish the study domain of the dataset ('Time' or 'Frequency')

        Returns:
            Surge and Sway comparison graphs, for all sea states
        """

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

                    # For the time being, only healthy state (1) and the first simulations of 30m dragging (2) are allowed to be compared.
                    if filename.replace('case', '1') in df.columns and filename.replace('case', '2') in df.columns:
                        ax.plot(df[domain], df[filename.replace('case', '1')], color='b', label='Healthy')
                        ax.plot(df[domain], df[filename.replace('case', '2')], color='r', label='Dragging', alpha=0.5)

                        #this condition only makes sense in the frequency domain.
                        if domain == 'Frequency':
                            ax.set_xlim(0, 0.15)
                        
                        ax.set_title(f'{h}_{t}_{dir}') #Subplot title
                        ax.legend(['Healthy', 'Dragging'], loc='upper right', bbox_to_anchor=(0.85, 0.9))

                        subplot_index +=1

        # Ajusta el espacio entre los subplots
        plt.subplots_adjust(top=1.4,bottom=1.2, hspace=hspace, wspace=wspace)

        # Agrega un título general y una leyenda
        plt.suptitle(f'Comparativa de estados de la plataforma en {mov}',y=1,fontsize=14)
        plt.tight_layout()

        # Muestra el gráfico
        plt.show()
