import numpy as np 
import cv2
import time
import threading
from Glasses_UFG_1 import Glasses_UFG
import os


class Pupilometer_UFG:

    PORTA_COM = ""
    ARCHIVE_VIDEO_PATH = ""
    path_configuracao = ""
    if os.name=='nt':         
        path_configuracao = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\configuracao.txt'      
    else:
        path_configuracao = os.path.dirname(os.path.abspath(__file__)) + '/Config_Pupilometro/configuracao.txt'

    print (path_configuracao)
    arquivo = open(path_configuracao, 'r')
    #linhas = arquivo.readlines()

    while arquivo.readline():
        line = arquivo.readline()
        param = line.split('|')        
        if param[0] == 'ARCHIVE_VIDEO_PATH':
            ARCHIVE_VIDEO_PATH = param[1]
        elif param[0] == 'PORTA_COM':
            PORTA_COM = param[1]

    for ln in arquivo.readline():
        param = ln.split('|')        
        if param[0] == 'ARCHIVE_VIDEO_PATH':
            ARCHIVE_VIDEO_PATH = param[1]
        elif param[0] == 'PORTA_COM':
            PORTA_COM = param[1]
    
    # This will return video from the first webcam on your computer. 
    cap_cam1 = cv2.VideoCapture(1)
    cap_cam2 = cv2.VideoCapture(2)

    # Define the codec and create VideoWriter object 
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    out_cam1 = cv2.VideoWriter(ARCHIVE_VIDEO_PATH+'\output_cam1.avi', fourcc, 30, (640, 480))  
    out_cam2 = cv2.VideoWriter(ARCHIVE_VIDEO_PATH+'\output_cam2.avi', fourcc, 30, (640, 480))  

    ini = time.time()

    fps = cap_cam1.get(cv2.CAP_PROP_FPS) # Return fram rate
    WIDTH = cap_cam1.get(cv2.CAP_PROP_FRAME_WIDTH)
    HEIGHT = cap_cam1.get(cv2.CAP_PROP_FRAME_HEIGHT)

    cap_cam1.set(cv2.CAP_PROP_FPS, 30) # Set fram rate

    print("FPS::{0} | WIDTH::{1} | HEIGHT:{2}".format(fps, WIDTH, HEIGHT))

    oculos = Glasses_UFG()
    oculos.connect(PORTA_COM, 9600)
    
    def start_exam():
    
        #Star thread que ira controlar os leds 
        thread = threading.Thread(target = oculos.ExecuteProtocol, args=[2, True, True, "3;0.033R;10;0.033G;10;0.033B;10;0.033W;10"])

        # loop runs if capturing has been initialized.
        num_frame = 1
        start = True
        while(True):

            # reads frames from a camera  
            # ret checks return at each frame 
            ret_cam1, frame_cam1 = cap_cam1.read()  
            ret_cam2, frame_cam2 = cap_cam2.read() 

            if start:
                thread.start()
                ini = time.time()
                start = False

            second =  (time.time() - ini) 
            cv2.putText(frame_cam1, ("FRAME: %s   Second: %.3f" % (num_frame,  second)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(frame_cam2, ("FRAME: %s   Second: %.3f" % (num_frame,  second)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            # output the frame 
            out_cam1.write(frame_cam1)  
            out_cam2.write(frame_cam2)      

            num_frame = num_frame + 1
            # Wait for 'a' key to stop the program  
            if cv2.waitKey(1) & 0xFF == ord('a'): 
                break  

            if not thread.is_alive():
                oculos.beep(True)
                time.sleep(0.2)
                oculos.beep(False)
                oculos.disconnect()
                break

        # Close the window / Release webcam 
        cap_cam1.release() 
        cap_cam2.release()

        # De-allocate any associated memory usage  
        cv2.destroyAllWindows() 


if __name__ == '__main__':
    c = Pupilometer_UFG()
    c.start_exam()