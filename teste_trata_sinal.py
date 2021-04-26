import funcao_trata_sinal as tr
import numpy as np
import time

nomeArquivo = 'arquivo_frame_diametro'
tipoArquivo = 'csv'

Arquivo = open(nomeArquivo + '.' + tipoArquivo, 'r')
Arquivo_Tratado = open(nomeArquivo + '_Tratado.' + tipoArquivo, 'w')

Tabela = []

x = []
y = []

for linha in Arquivo:
    x.append(int(linha.split(';')[0]))#Eixo x fica os frames
    y.append(int(linha.split(';')[1]))#Eixo y fica os diametros


# x é o numero do frame e y o diametro
xNew = tr.tratar_new(x, y)

i = 0
for row in xNew:
    Arquivo_Tratado.write(str(i)+";"+str(int(row)))
    Arquivo_Tratado.write("\n")
    i = i + 1