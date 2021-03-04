import cv2
import argparse
import imutils
import numpy as np
from matplotlib import pyplot as plt
import sys


def funcao_identifica_pupila(img_input, num_frame, fps):

    img = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)

    # Filtro gaussiano
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Thresholding global
    ret, img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY_INV)
    #ret,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))

    # Transformação morfológica FECHAR
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    # Transformação morfológica ABRIR
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    # Encontrar contornos na imagem
    cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    new_img = img_input.copy()

    # Contar as areas de contorno
    area_array = np.zeros(len(cnts))
    counter = 0
    for cnt in cnts:
        area_array[counter] = cv2.contourArea(cnt)
        counter += 1

    # Verifica se encontrou alguma
    if area_array.size == 0:
        return new_img

    # Pegar a maior area e tira o raio e o centro
    max_area_index = np.argmax(area_array)
    cnt = cnts[max_area_index]
    (x, y), radius = cv2.minEnclosingCircle(cnt)

    if radius < 20:
        return new_img

    # Desenha o contorno e na imagem
    cv2.drawContours(new_img, [cnt], -1, (0, 0, 255), 2)
    cv2.putText(new_img, ("Center(x:%.0f | y:%.0f) Raio:%.3f  FRAME: %s   FPS: %s" % (
        x, y, radius, num_frame,  fps)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    return new_img
