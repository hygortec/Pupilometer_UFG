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
	path_exame = ""
	path_protocolo = ""
	LEFT_CAM = 0
	RIGHT_CAM = 1
	SEQUENTIAL = 1

	if os.name=='nt':         
		path_configuracao = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\configuracao.txt'  
		path_exame = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\exame.txt'     
		path_protocolo = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\protocolo.txt' 
	else:
		path_configuracao = os.path.dirname(os.path.abspath(__file__)) + '/Config_Pupilometro/configuracao.txt'
		path_exame = os.path.dirname(os.path.abspath(__file__)) + '/Config_Pupilometro/exame.txt'
		path_protocolo = os.path.dirname(os.path.abspath(__file__)) + '/Config_Pupilometro/protocolo.txt'

	print (path_configuracao)
	arquivo = open(path_configuracao, 'r')
	
	for ln in arquivo:
		param = ln.split('=')        
		if param[0] == 'ARCHIVE_VIDEO_PATH':
			ARCHIVE_VIDEO_PATH = param[1].replace("\n", "")
		elif param[0] == 'PORTA_COM':
			PORTA_COM = param[1].replace("\n", "")
		elif param[0] == 'LEFT_CAM':
			LEFT_CAM = param[1].replace("\n", "")
		elif param[0] == 'RIGHT_CAM':
			RIGHT_CAM = param[1].replace("\n", "")
		elif param[0] == 'SEQUENTIAL':
			SEQUENTIAL = int(param[1].replace("\n", ""))
			
	
	# This will return video from the first webcam on your computer. 
	cap_cam1 = cv2.VideoCapture(int(LEFT_CAM))
	cap_cam2 = cv2.VideoCapture(int(RIGHT_CAM))

	ini = time.time()

	fps = cap_cam1.get(cv2.CAP_PROP_FPS) # Return fram rate
	WIDTH = cap_cam1.get(cv2.CAP_PROP_FRAME_WIDTH)
	HEIGHT = cap_cam1.get(cv2.CAP_PROP_FRAME_HEIGHT)

	cap_cam1.set(cv2.CAP_PROP_FPS, 30) # Set fram rate

	print("FPS::{0} | WIDTH::{1} | HEIGHT:{2}".format(fps, WIDTH, HEIGHT))

	def start_exam(self, eyes, eyes_stim):
		global oculos, PORTA_COM, SEQUENTIAL
		
		oculos = Glasses_UFG()
		oculos.connect(self.PORTA_COM, 9600)

		# Define the codec and create VideoWriter object 
		#fourcc = cv2.VideoWriter_fourcc(*'XVID')
		fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
		if(eyes == 0):
			out_cam1 = cv2.VideoWriter(self.ARCHIVE_VIDEO_PATH+'\output_cam1_'+str(self.SEQUENTIAL)+'.avi', fourcc, 30, (640, 480))  
		elif(eyes == 1):
			out_cam2 = cv2.VideoWriter(self.ARCHIVE_VIDEO_PATH+'\output_cam2_'+str(self.SEQUENTIAL)+'.avi', fourcc, 30, (640, 480)) 
		elif(eyes == 2):
			out_cam1 = cv2.VideoWriter(self.ARCHIVE_VIDEO_PATH+'\output_cam1_'+str(self.SEQUENTIAL)+'.avi', fourcc, 30, (640, 480))  
			out_cam2 = cv2.VideoWriter(self.ARCHIVE_VIDEO_PATH+'\output_cam2_'+str(self.SEQUENTIAL)+'.avi', fourcc, 30, (640, 480)) 
		
		print(self.SEQUENTIAL)

		#Star thread que ira controlar os leds 
		thread = threading.Thread(target = oculos.ExecuteProtocol, args=[eyes_stim, True, True, "3;0.033R;10;0.033G;10;0.033B;10;0.033W;10"])
		
		# loop runs if capturing has been initialized.
		num_frame = 1
		start = True
		while(True):

			# reads frames from a camera  
			# ret checks return at each frame 
			if(eyes == 0):
				ret_cam1, frame_cam1 = self.cap_cam1.read() 				
			elif(eyes == 1):			
				ret_cam2, frame_cam2 = self.cap_cam2.read()
			elif(eyes == 2):
				ret_cam1, frame_cam1 = self.cap_cam1.read()  
				ret_cam2, frame_cam2 = self.cap_cam2.read()

			if start:
				thread.start()
				ini = time.time()
				start = False

			second =  (time.time() - ini) 

			if(eyes == 0):
				cv2.putText(frame_cam1, ("LEFT FRAME: %s   Second: %.3f" % (num_frame,  second)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)						
			elif(eyes == 1):			
				cv2.putText(frame_cam2, ("RIGHT FRAME: %s   Second: %.3f" % (num_frame,  second)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
			elif(eyes == 2):
				cv2.putText(frame_cam1, ("LEFT FRAME: %s   Second: %.3f" % (num_frame,  second)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
				cv2.putText(frame_cam2, ("RIGHT FRAME: %s   Second: %.3f" % (num_frame,  second)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

			# output the frame 
			if(eyes == 0):
				out_cam1.write(frame_cam1)  
			elif(eyes == 1):			
				out_cam2.write(frame_cam2)   
			elif(eyes == 2):
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
		
		if(eyes == 0):
			self.cap_cam1.release() 
		elif(eyes == 1):			
			self.cap_cam2.release() 
		elif(eyes == 2):
			self.cap_cam1.release() 
			self.cap_cam2.release()

		# De-allocate any associated memory usage  
		cv2.destroyAllWindows() 
		SEQUENTIAL = self.update_sequential(self.SEQUENTIAL)

	def preview(self, _frame_cam1, _frame_cam2):
	
		global oculos,PORTA_COM
		oculos = Glasses_UFG()
		oculos.connect(self.PORTA_COM, 9600)
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

			_frame_cam1 = frame_cam1
			_frame_cam2 = frame_cam2

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

	def update_sequential(self, sequential):
		global SEQUENTIAL
		# Read in the file
		with open(self.path_configuracao, 'r') as file :
  			filedata = file.read()

		# Replace the target string
		filedata = filedata.replace('SEQUENTIAL='+str(sequential), 'SEQUENTIAL='+str(sequential+1))

		# Write the file out again
		with open(self.path_configuracao, 'w') as file:
  			file.write(filedata)

		return self.SEQUENTIAL + 1
   
if __name__ == '__main__':
	c = Pupilometer_UFG()
	c.start_exam(0, 0)