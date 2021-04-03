from flask import Flask, render_template, request, redirect
import os
from flask import Response
import threading
import argparse
import datetime
import imutils
import time
import cv2
from Glasses_UFG_1 import Glasses_UFG 
from Pupilometer_UFG import Pupilometer_UFG

app = Flask(__name__)

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
t = threading
stop = False
outputFrame_letf = None
outputFrame_right = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)
# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()

path_configuracao = ""
path_exame = ""
path_protocolo = ""

if os.name=='nt':         
 path_configuracao = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\configuracao.txt'
 path_exame = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\exame.txt'
 path_protocolo = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\protocolo.txt' 
else:
 path_configuracao = os.path.dirname(os.path.abspath(__file__)) + '/Config_Pupilometro/configuracao.txt'
 path_exame = os.path.dirname(os.path.abspath(__file__)) + '/Config_Pupilometro/exame.txt'
 path_protocolo = os.path.dirname(os.path.abspath(__file__)) + '/Config_Pupilometro/protocolo.txt'


cam_left = None
cam_right = None

time.sleep(2.0)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/protocolo')
def protocolo():
	protocol = ""
	Intensity_Red ="0"
	Intensity_Green = "0"
	Intensity_Blue = "0"
	Intensity_White = "0"
	arquivo = open(path_protocolo, 'r')
	for linha in arquivo:
		if "protocol" in linha:
			protocol = linha.split('=')[1].replace("\n", "")
		elif "Intensity_Red" in linha:
			Intensity_Red = linha.split('=')[1].replace("\n", "")
		elif "Intensity_Green" in linha:
			Intensity_Green = linha.split('=')[1].replace("\n", "")
		elif "Intensity_Blue" in linha:
			Intensity_Blue = linha.split('=')[1].replace("\n", "")
		elif "Intensity_White":
			Intensity_White = linha.split('=')[1].replace("\n", "")

	dados=[protocol, Intensity_Red, Intensity_Green, Intensity_Blue, Intensity_White]
	
	return render_template('protocolo.html', data=dados)

@app.route('/test_protocolo')
def test_protocolo():
	protocol = ""
	PORTA_COM = ""
	
	arquivo = open(path_protocolo, 'r')
	for linha in arquivo:
		if "protocol" in linha:
			protocol = linha.split('=')[1].replace("\n", "")
		
	arquivo = open(path_configuracao, 'r')
	for linha in arquivo:
		if "PORTA_COM" in linha:
			PORTA_COM = linha.split('=')[1].replace("\n", "")
	
	oculos = Glasses_UFG()
	oculos.connect(PORTA_COM, 9600)

	oculos.ExecuteProtocol(2, True, True, "3;0.033R;10;0.033G;10;0.033B;10;0.033W;10")

	#return render_template('protocolo.html')

@app.route('/exame')
def exame():    
 stop_preview()
 return render_template('exame.html')

@app.route('/settings')
def settings():
	ARCHIVE_VIDEO_PATH = ""
	PORTA_COM ="0"
	LEFT_CAM = "0"
	RIGHT_CAM = "0"
	
	arquivo = open(path_configuracao, 'r')
	for linha in arquivo:
		if "ARCHIVE_VIDEO_PATH" in linha:
			ARCHIVE_VIDEO_PATH = linha.split('=')[1].replace("\n", "")
		elif "PORTA_COM" in linha:
			PORTA_COM = linha.split('=')[1].replace("\n", "")
		elif "LEFT_CAM" in linha:
			LEFT_CAM = linha.split('=')[1].replace("\n", "")
		elif "RIGHT_CAM" in linha:
			RIGHT_CAM = linha.split('=')[1].replace("\n", "")		

	dados=[ARCHIVE_VIDEO_PATH, PORTA_COM, LEFT_CAM, RIGHT_CAM]
	
	return render_template('settings.html', data=dados)    


@app.route('/preview')
def preview():    
	global t, stop
	t = threading.Thread(target=start_preview)
	t.daemon = True	
	t.start()
	
	return render_template('preview.html')

@app.route('/salvar_protocolo', methods=['GET','POST'])
def salvar_protocolo():
 if request.method == 'POST':
  print (path_protocolo)
  arquivo = open(path_protocolo, 'w')
  arquivo.write("protocol="+ request.form['protocol'] +"\n")
  arquivo.write("Intensity_Red="+request.form['Intensity_Red']+"\n")
  arquivo.write("Intensity_Green="+request.form['Intensity_Green']+"\n")
  arquivo.write("Intensity_Blue="+request.form['Intensity_Blue']+"\n")
  arquivo.write("Intensity_White="+request.form['Intensity_White']+"\n")
  arquivo.close()
  
 return redirect("/")

@app.route('/salvar_configuracao', methods=['GET','POST'])
def salvar_configuracao():
 if request.method == 'POST':
  
  arquivo = open(path_configuracao, 'w')
  arquivo.write("ARCHIVE_VIDEO_PATH="+ request.form['path'] +"\n")
  arquivo.write("PORTA_COM="+request.form['port']+"\n")
  arquivo.write("LEFT_CAM="+request.form['left_camera']+"\n")
  arquivo.write("RIGHT_CAM="+request.form['right_camera']+"\n")
  
  arquivo.close()
  
 return redirect("/")


@app.route('/executar_exame', methods=['GET', 'POST'])
def executar_exame():
 if request.method == 'POST':
	 estimulo = request.form['stimulated']
	 gravar = request.form['record']
	
	 pupilometro = Pupilometer_UFG()
	 pupilometro.start_exam(int(gravar), int(estimulo))

 return redirect("/")

def start_preview():
	# grab global references to the video stream, output frame, and
	# lock variables
	global cam_left, cam_right, outputFrame_letf, outputFrame_right, lock, stop

	LEFT_CAM = 0
	RIGHT_CAM = 1
	arquivo = open(path_configuracao, 'r')
	for linha in arquivo:
		if "ARCHIVE_VIDEO_PATH" in linha:
			ARCHIVE_VIDEO_PATH = linha.split('=')[1].replace("\n", "")
		elif "PORTA_COM" in linha:
			PORTA_COM = linha.split('=')[1].replace("\n", "")
		elif "LEFT_CAM" in linha:
			LEFT_CAM = linha.split('=')[1].replace("\n", "")
		elif "RIGHT_CAM" in linha:
			RIGHT_CAM = linha.split('=')[1].replace("\n", "")		

	cam_left = cv2.VideoCapture(int(LEFT_CAM))
	cam_right = cv2.VideoCapture(int(RIGHT_CAM))


	stop = False
	# loop over frames from the video stream
	while stop== False:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it		

		ret_cam1, frame_left = cam_left.read()  
		ret_cam2, frame_right = cam_right.read() 

		with lock:
			outputFrame_letf = frame_left.copy()
			outputFrame_right = frame_right.copy()

	cam_left.release
	cam_right.release

def start_preview_v2():
	# grab global references to the video stream, output frame, and
	# lock variables
	global cam_left, cam_right, outputFrame_letf, outputFrame_right, lock, stop
	
	pupilometro = Pupilometer_UFG()
	pupilometro.start_exam(0)



def stop_preview():
 # grab global references to the video stream, output frame, and
 # lock variables
 global stop, t
 stop = True
 outputFrame_letf = None
 outputFrame_right = None

def generate_left():
	# grab global references to the output frame and lock variables
	global outputFrame_letf, lock, stop
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame_letf is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame_letf)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

def generate_right():
	# grab global references to the output frame and lock variables
	global outputFrame_right, lock, stop
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame_right is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame_right)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed_left")
def video_feed_left():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate_left(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/video_feed_right")
def video_feed_right():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate_right(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
	
	# start the flask app
	app.run(host="0.0.0.0", port="80", debug=True, threaded=True, use_reloader=False)
# release the video stream pointer
