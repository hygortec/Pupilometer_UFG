import funcao_identifica_pupila as ft
import trata_sinal as tr
import numpy as np
import cv2
import time

cap = cv2.VideoCapture("C:\\Eyes\\3\\30;1W;300;1R;300;1G;300;1B;300_L.avi")

arquivo =  open('C:\\Eyes\\3\\30;1W;300;1R;300;1G;300;1B;300_L.csv','w')
arquivo2 = open('C:\\Eyes\\3\\30;1W;300;1R;300;1G;300;1B;300_L_tratado.csv','w')

vet = []
count = 0
while(True):
    # Capturar frame a frame
    ret, frame = cap.read()

    #Esquerdo
    y=200
    x=200
    h=200
    w=350

    #Direito
    y=125
    x=125
    h=200
    w=350


    if ret == True:
        img_in = frame[y:y+h, x:x+w]    

        #img = img_in
        img, raio = ft.funcao_identifica_pupila(count, img_in)
        vet.append(int(raio))
    else:

        break

    # Exibir o frame resultante
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break
    
    count= count +1
    
for i in range(len(vet)):
        arquivo.write(str(i)+";"+str(vet[i])+'\n')

new_vet = tr.tratar(vet)
for i in range(len(new_vet)):
            arquivo2.write(str(i)+";"+str(int(new_vet[i]))+'\n')




# Quando tudo estiver pronto, libere a captura
cap.release()
cv2.destroyAllWindows()



