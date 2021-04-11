import funcao_identifica_pupila as ft
import numpy as np
import cv2

cap = cv2.VideoCapture("video.mp4")

while(True):
    # Capturar frame a frame
    ret, frame = cap.read()

    img = ft.funcao_identifica_pupila(frame)

    # Exibir o frame resultante
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Quando tudo estiver pronto, libere a captura
cap.release()
cv2.destroyAllWindows()



