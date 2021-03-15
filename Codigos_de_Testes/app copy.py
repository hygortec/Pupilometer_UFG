from flask import Flask, render_template, request, redirect
import os
from imutils.video import VideoStream
from flask import Response
import threading
import argparse
import datetime
import imutils
import time
import cv2

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
cam_left = VideoStream(src=0)
cam_right = VideoStream(src=1)

time.sleep(2.0)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/protocolo')
def protocolo():
    return render_template('protocolo.html')

@app.route('/exame')
def exame():    
    stop_preview()
    return render_template('exame.html')

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
        protocol = request.form['protocol'] 
        Intensity_Red = request.form['Intensity_Red']
        Intensity_Green = request.form['Intensity_Green']
        Intensity_Blue = request.form['Intensity_Blue']
        Intensity_White = request.form['Intensity_White']

        new_path = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\protocolo.txt'      

        print (new_path)
        arquivo = open(new_path, 'w')
        arquivo.write("protocol:"+protocol+"\n")
        arquivo.write("Intensity_Red:"+Intensity_Red+"\n")
        arquivo.write("Intensity_Green:"+Intensity_Green+"\n")
        arquivo.write("Intensity_Blue:"+Intensity_Blue+"\n")
        arquivo.write("Intensity_White:"+Intensity_White+"\n")
        arquivo.close()
        print (protocol+"\n")
        print (Intensity_Red+"\n")
        print (Intensity_Green+"\n")
        print (Intensity_Blue+"\n")
        print (Intensity_White+"\n")
    return redirect("/")

@app.route('/executar_exame', methods=['GET','POST'])
def executar_exame():
    if request.method == 'POST':
        estimulo = request.form['stimulated'] 
        gravar = request.form['record']

        new_path = os.path.dirname(os.path.abspath(__file__)) + '\\Config_Pupilometro\\exame.txt'      

        print (new_path)
        arquivo = open(new_path, 'w')
        arquivo.write(estimulo+";"+gravar)
        print (protocolo)
    return redirect("/")

def start_preview():
	# grab global references to the video stream, output frame, and
	# lock variables
	global cam_left, cam_right, outputFrame_letf, outputFrame_right, lock, stop


	stop = False
	# loop over frames from the video stream
	while stop== False:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame_left = cam_left.read()
		frame_right = cam_right.read()

		with lock:
			outputFrame_letf = frame_left.copy()
			outputFrame_right = frame_right.copy()

def stop_preview():
    # grab global references to the video stream, output frame, and
    # lock variables
    global stop, t
    stop = True

def generate_left():
	# grab global references to the output frame and lock variables
	global outputFrame_letf, lock
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
	global outputFrame_right, lock
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
	app.run(host="0.0.0.0", port="5000", debug=True, threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()