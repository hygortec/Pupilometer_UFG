import argparse
import imutils
import numpy as np
from matplotlib import pyplot as plt
import sys
from scipy.interpolate import interp1d
from urllib.request import urlopen


def tratar(vetor):
    vetor = retira_outlier(vetor)
    vetor = interpolar(vetor)
    return vetor
    higor

def tratar_new(x, y):

    y = retira_outlier(y)
    vetor = interpolar(x, y)
    return vetor


def retira_outlier(vetor):

    # Copio o vetor retirando os zeros para fazer a media dos valores 
    new_vetor = []
    for i in range(len(vetor)):
        if vetor[i] != 0:
            new_vetor.append(vetor[i])

    media = np.mean(new_vetor)
    desvio_padrao = np.std(new_vetor)


    # Retira os outlier
    # Se o diametro da pupila for maior que o diametro anterior mais o desvio padrão eu coloco 0
    # ou se o diametro da pupila for menor que o diametro anterior menos o desvio padrão eu coloco 0
    for i in range(len(vetor)):
        if i == 0:
            if vetor[i] > media + desvio_padrao or vetor[i] < media - desvio_padrao:
                vetor[i] = int(media)

        else:
            if vetor[i-1] == 0:
                if vetor[i] > media + desvio_padrao or vetor[i] < media - desvio_padrao:
                    vetor[i] = 0

            elif (vetor[i] > vetor[i-1] + desvio_padrao) or (vetor[i] < vetor[i-1] - desvio_padrao):
                vetor[i] = 0        

    return vetor

def interpolar(x,y):

    xi = []
    yi = []

    i = 0
    while(i < len(x)):
        if(y[i] > 0): #Retira os zeros
            xi.append(x[i]) #Eixo x fica os frames
            yi.append(y[i]) #Eixo y fica os diametros
        i = i + 1

    # Interpolando pontos em toda a função.
    interpolacao_linear = interp1d(xi, yi, kind= 'linear', fill_value="extrapolate")

    #Depois que a função foi mapeada é só chamar para fazer a interpolação dos dados que faltava
    interpolacao_adjclose = interpolacao_linear(x)

    return interpolacao_adjclose   
    