import numpy as np 
import cv2
  
# This will return video from the first webcam on your computer. 
cap_cam1 = cv2.VideoCapture(0)
cap_cam2 = cv2.VideoCapture(2)

# Define the codec and create VideoWriter object 
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out_cam1 = cv2.VideoWriter('C:\Eyes\output_cam1.avi', fourcc, 30, (640, 480))  
out_cam2 = cv2.VideoWriter('C:\Eyes\output_cam2.avi', fourcc, 30, (640, 480))  



# loop runs if capturing has been initialized.  
cont = 0
while(cont < 300):
    # reads frames from a camera  
    # ret checks return at each frame 
    ret_cam1, frame_cam1 = cap_cam1.read()  
    ret_cam2, frame_cam2 = cap_cam2.read()  

    # output the frame 
    out_cam1.write(frame_cam1)  
    out_cam2.write(frame_cam2)  
    
    cont = cont + 1
    # Wait for 'a' key to stop the program  
    if cv2.waitKey(1) & 0xFF == ord('a'): 
        break

# Close the window / Release webcam 
cap_cam1.release() 
cap_cam2.release()

# De-allocate any associated memory usage  
cv2.destroyAllWindows() 