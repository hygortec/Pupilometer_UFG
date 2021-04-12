import numpy as np 
import cv2
import time
  
# This will return video from the first webcam on your computer. 
cap_cam1 = cv2.VideoCapture(1)

# Define the codec and create VideoWriter object 
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

width = 1024
height = 768
fps = 60
cap_cam1.set(cv2.CAP_PROP_FOURCC, fourcc)
cap_cam1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap_cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap_cam1.set(cv2.CAP_PROP_FPS, fps)

out_cam1 = cv2.VideoWriter('C:\Eyes\output_cam1.avi', fourcc, fps, (width, height))  

tempo_ini = time.time()
# loop runs if capturing has been initialized.  
cont = 0
while(True):
    # reads frames from a camera  
    # ret checks return at each frame 
    ret_cam1, frame_cam1 = cap_cam1.read()    
    
    cont = cont + 1

    second =  (time.time() - tempo_ini) 
    cv2.putText(frame_cam1, ("FRAME: %s | Second: %.3f | FPS: %0.3f" % (cont,  second, cont/second )), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # output the frame 
    out_cam1.write(frame_cam1)  

    cv2.imshow("Cap", frame_cam1)

    # Wait for 'a' key to stop the program  
    if cv2.waitKey(1) & 0xFF == ord('a'): 
        break

# Close the window / Release webcam 
cap_cam1.release() 

# De-allocate any associated memory usage  
cv2.destroyAllWindows() 