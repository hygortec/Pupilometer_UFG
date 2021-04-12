import cv2
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

def retira_outlier(vetor):

    desvio_padrao = np.std(vetor)
    media = np.mean(vetor)

    # Se o diametor da pupila for maior que o diametro anterior mais o desvio padrão eu coloco 0
    # ou se o diametor da pupila for menor que o diametro anterior menos o desvio padrão eu coloco 0
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

def interpolar(vetor):
   
    xi = []
    yi = []
    x = []

    i = 0
    while(i < len(vetor)):
        if(vetor[i] != 0):
            xi.append(i) #Eixo x fica os frames
            yi.append(vetor[i]) #Eixo y fica os diametros
        
        x.append(i)
        i = i+1

    # Interpolando pontos em toda a função.
    interpolacao_linear = interp1d(xi, yi, kind='linear')

    #Depois que a função foi mapeada é só chamar para fazer a interpolação dos dados que faltava
    interpolacao_adjclose = interpolacao_linear(x)

    return interpolacao_adjclose