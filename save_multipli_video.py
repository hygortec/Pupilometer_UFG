import numpy as np 
import cv2
import time
  
# This will return video from the first webcam on your computer. 
cap_cam1 = cv2.VideoCapture(0)
cap_cam2 = cv2.VideoCapture(1)

# Define the codec and create VideoWriter object 
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

out_cam1 = cv2.VideoWriter('C:\Eyes\output_cam1.avi', fourcc, 30, (640, 480))  
out_cam2 = cv2.VideoWriter('C:\Eyes\output_cam2.avi', fourcc, 30, (640, 480))  

ini = time.time()

fps = cap_cam1.get(cv2.CAP_PROP_FPS) # Return fram rate
WIDTH = cap_cam1.get(cv2.CAP_PROP_FRAME_WIDTH)
HEIGHT = cap_cam1.get(cv2.CAP_PROP_FRAME_HEIGHT)


cap_cam1.set(cv2.CAP_PROP_FPS, 30) # Set fram rate

print("FPS::{0} | WIDTH::{1} | HEIGHT:{2}".format(fps, WIDTH, HEIGHT))

# loop runs if capturing has been initialized.  
cont = 0
num_frame = 1
while(cont < 300):
    # reads frames from a camera  
    # ret checks return at each frame 
    ret_cam1, frame_cam1 = cap_cam1.read()  
    ret_cam2, frame_cam2 = cap_cam2.read()  
    
    second =  (time.time() - ini) 
    cv2.putText(frame_cam1, ("FRAME: %s   Second: %.3f" % (num_frame,  second)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(frame_cam2, ("FRAME: %s   Second: %.3f" % (num_frame,  second)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # output the frame 
    out_cam1.write(frame_cam1)  
    out_cam2.write(frame_cam2)  
       
    cont = cont + 1
    num_frame = num_frame + 1
    # Wait for 'a' key to stop the program  
    if cv2.waitKey(1) & 0xFF == ord('a'): 
        break

# Close the window / Release webcam 
cap_cam1.release() 
cap_cam2.release()

# De-allocate any associated memory usage  
cv2.destroyAllWindows() 