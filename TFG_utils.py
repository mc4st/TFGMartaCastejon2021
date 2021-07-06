#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from scipy import signal
from mne.time_frequency import psd_welch

# Listado de los ficheros directorio
def extract_files(EEG_path):
    file_list = os.listdir(EEG_path)
    return file_list
    
# Lee el nombre del fichero vmrk
def take_vmrk_filename(EEG_path):
    file_list = extract_files(EEG_path)
    for file in file_list:
        if file.split(".")[1]== "vmrk":
            vmrk_filename = os.path.join(EEG_path, file)
    return vmrk_filename

# Lee el nombre del fichero vmrk
def take_vhdr_filename(EEG_path):
    file_list = extract_files(EEG_path)
    for file in file_list:
        if file.split(".")[1]== "vhdr":
            vhdr_filename = os.path.join(EEG_path, file)
    return vhdr_filename

def take_eeg_filename(EEG_path):
    file_list = extract_files(EEG_path)
    for file in file_list:
        if file.split(".")[1]== "eeg":
            eeg_filename = os.path.join(EEG_path, file)
    return eeg_filename


## Calculo de la densidad espectral de potencia por canal y banda de frecuencia

def get_dep_channel(datos_signal,fs,i):
    datos = datos_signal.get_data()
    num_canales = datos.shape[0]
    potencia_por_canal = []
    for num in range(0,num_canales):
        f,Px=signal.periodogram(datos[i], fs, window='hamming')
        potencia_por_canal.append(sum(Px)*f[1])    
        idx = []
        for cont in f:
            if cont>0:
                idx.append(True)
            else:
                idx.append(False)
    
    return potencia_por_canal, idx, f, Px

def get_dep_channel_bandas(datos_signal,fs):
    
    datos = datos_signal.get_data()
    num_canales = datos.shape[0]
    
    potencia_por_canal = []
    potencia_banda_delta = []
    potencia_banda_theta = []
    potencia_banda_alpha = []
    potencia_banda_beta = []
    potencia_banda_gamma = []
    
    for i in range(0,num_canales):
        f,Px=signal.periodogram(datos[i], fs, window='hamming')
        indice_Px = []
        for j in f:
            if j>0.5 and j<40:
                indice_Px.append(True)
            else:
                indice_Px.append(False)
        id_Px = sum(Px[indice_Px]*f[1])
        potencia_por_canal.append(id_Px)

                
        #BANDA DELTA
        
        indice_delta = []
        for j in f:
            if j>3 and j<4:
                indice_delta.append(True)
            else:
                indice_delta.append(False)
        delta = sum(Px[indice_delta]*f[1])
        potencia_banda_delta.append(delta)
        
        #BANDA THETA
        
        indice_theta = []
        for j in f:
            if j>4 and j<7:
                indice_theta.append(True)
            else:
                indice_theta.append(False)
        theta = sum(Px[indice_theta]*f[1])
        potencia_banda_theta.append(theta)
        
        #BANDA ALPHA
        
        indice_alpha = []
        for j in f:
            if j>7 and j<13:
                indice_alpha.append(True)
            else:
                indice_alpha.append(False)
        alpha = sum(Px[indice_alpha]*f[1])
        potencia_banda_alpha.append(alpha)
        
        #BANDA BETA
        
        indice_beta = []
        for j in f:
            if j>13 and j<30:
                indice_beta.append(True)
            else:
                indice_beta.append(False)
        beta = sum(Px[indice_beta]*f[1])
        potencia_banda_beta.append(beta)
        
        #BANDA GAMMA
        
        indice_gamma = []
        for j in f:
            if j>30 and j<40:
                indice_gamma.append(True)
            else:
                indice_gamma.append(False)
        gamma = sum(Px[indice_gamma]*f[1])
        potencia_banda_gamma.append(gamma)
        
    return potencia_por_canal, potencia_banda_delta, potencia_banda_theta, potencia_banda_alpha, potencia_banda_beta, potencia_banda_gamma, f, Px

#Ratio Espectro de la potencia por bandas

def get_ratio(pot_por_canal, pot_bandas):

    pot_delta = pot_bandas[0]
    ratio_delta = []
    pot_theta = pot_bandas[1]
    ratio_theta = []
    pot_alpha = pot_bandas[2]
    ratio_alpha = []
    pot_beta = pot_bandas[3]
    ratio_beta = []
    pot_gamma = pot_bandas[4]
    ratio_gamma = []
    
    for i in range(0, 31):
        div_delta = pot_delta[i]/pot_por_canal[i]
        ratio_delta.append(div_delta)
    
    for i in range(0, 31):
        div_theta = pot_theta[i]/pot_por_canal[i]
        ratio_theta.append(div_theta)
        
    for i in range(0, 31):
        div_alpha = pot_alpha[i]/pot_por_canal[i]
        ratio_alpha.append(div_alpha)
        
    for i in range(0, 31):
        div_beta = pot_beta[i]/pot_por_canal[i]
        ratio_beta.append(div_beta)
        
    for i in range(0, 31):
        div_gamma = pot_gamma[i]/pot_por_canal[i]
        ratio_gamma.append(div_gamma)

    
    return ratio_delta, ratio_theta, ratio_alpha, ratio_beta, ratio_gamma
