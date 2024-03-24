import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import shutil
from scipy.fft import fft, fftfreq

class Preprocess:

    def __init__(self, movements = ['Surge', 'Sway'], main_path = rf'D:\arturo_sim\simulaciones\acoplado',dataframes_surge = {}, dataframes_sway ={}):
        self.movements = movements
        self.main_path = main_path
        self.Hs =  ['Hs1','Hs2']
        self.Tp = ['Tp2','Tp3']
        self.direction = ['dir1','dir2']
        self.cases = ['1','2']
        self.dataframes_surge = dataframes_surge
        self.dataframes_sway = dataframes_sway
        self.stabilizing_signal()


    def create_gid_files(self):

        gid_template = os.path.join(self.main_path,'oc4_0_1.gid')

        for h in self.Hs:
            for t in self.Tp:
                for dir in self.direction:
                    for case in self.cases:

                        path =  os.path.join(self.main_path,'pruebas', f'oc4__{h}__{t}__{dir}__{case}.gid')
                        shutil.copytree(gid_template, path)
                        archivos = os.listdir(path)
                        
                        for archivo in archivos:
                            if archivo.startswith('oc4_0_1'):
                                # Replace gid name
                                nuevo_nombre = archivo.replace('oc4_0_1',f'oc4__{h}__{t}__{dir}__{case}')

                                # Rename all gid filenames
                                viejo_path = os.path.join(path, archivo)
                                nuevo_path = os.path.join(path, nuevo_nombre)

                                os.rename(viejo_path, nuevo_path)


    def extract_res_files(self):

        # Open and extract timeseries.res information and transform in .txt file
        for h in self.Hs:
            for t in self.Tp:
                for dir in self.direction:
                    for case in self.cases:

                        simulacion = f'oc4__{h}__{t}__{dir}__{case}'
                        res_path = os.path.join(self.main_path,'pruebas',f'{simulacion}.gid',f'{simulacion}.BodyKinematics.res')
                        with open(res_path,'rb') as res:
                            res_data = res.read().decode('utf-8', errors='ignore')
                        
                        # Write .res information in .txt
                        txt_path = os.path.join(self.main_path,'pruebas_txt',f'oc4__{h}__{t}__{dir}__{case}.txt')
                        with open(txt_path, 'w', encoding='utf-8') as txt_file:
                            txt_file.write(res_data)

                        # Store results in a dictionary of dataframes
                        df = pd.read_csv(txt_path, sep='\t', header=4).iloc[:,:7]
                        for mov in self.movements:
                            if mov == 'Surge':
                                self.dataframes_surge[simulacion] = df[['time[s]','Surge']]
                            else:
                                self.dataframes_sway[simulacion] = df[['time[s]','Sway']]
                            
        return self.dataframes_surge, self.dataframes_sway


    def stabilizing_signal(self):

        for direction, dataframes in {"Surge": self.dataframes_surge, "Sway": self.dataframes_sway}.items():
            for key, df in dataframes.items():
                for col in df.columns[1:]:
                    df[col] = df[col] - df[col].mean()
        
        return self.dataframes_surge, self.dataframes_sway
    

    def fourier_python(self):

        self.stabilizing_signal()

        for mov in self.movements:
            if mov == 'Surge':
                dataframes = self.dataframes_surge
            else:
                dataframes = self.dataframes_sway

            for key, df in dataframes.items():
                mov_data = df[mov].to_numpy()

                # Scipy fourier transform
                fft_mov = fft(mov_data)
                N = len(fft_mov)
                fft_freq = fftfreq(N, 0.1)[:N//2]
                amplitudes = 1/N * np.abs(fft_mov[0:N//2])

                # Update df
                df = pd.DataFrame({'Frequencies': fft_freq, 'Amplitudes': amplitudes})
                dataframes[key] = df


