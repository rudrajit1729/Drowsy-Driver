# python main.py --webcam webcam_index

# Import Libraries
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import os
import pyttsx3
import helpers

# CONSTANTS
EAR_THRESH = 0.3
EAR_CONSEC_FRAMES = 20
YAWN_THRESH = 20

# FLAGS AND COUNTERS
alert_status = False
alert_status2 = False
saying = False
COUNTER = 0

# Voice Engine - Pyttsx3
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices) - 1].id)

# Utility Function
def alert(msg):
	global alert_status
	global alert_status2
	global saying

	while alert_status:
		print("Call Driver")
		engine.say(msg)
		engine.runAndWait()

	if alert_status2:
		print("Call Driver")
		saying = True
		engine.say(msg)
		engine.runAndWait()
		saying = False

# Setting up Input Cam - Default set to Input Cam
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0, help="index of webcam on system")
args = vars(ap.parse_args())

# Load Predictor And Detector
print("Loading predictor and detector...")
# detector = dlib.get_frontal_face_detector()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")    #Faster but less accurate
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Start Video Stream
print("Starting Video Stream...")
# vs = VideoStream(0).start()
vs = VideoStream(src=args["webcam"]).start()
#vs= VideoStream(usePiCamera=True).start() # For Raspberry Pi
time.sleep(1.0)

# Main Loop
while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect Faces
	faces = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	for (x, y, w, h) in faces:
		face = dlib.rectangle(int(x), int(y), int(x + w),int(y + h))

		shape = predictor(gray, face)
		shape = face_utils.shape_to_np(shape)

		# Get Eye Aspect Ratio and Lip Distance
		ear, leftEye, rightEye = helpers.getEAR(shape)
		distance = helpers.getLipDist(shape)

		# Contour around eye region
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)

		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		# Contour around lips
		lips = shape[48:60]
		cv2.drawContours(frame, [lips], -1, (0, 255, 0), 1)

		# Check Drowsiness Threshold and trigger alert
		if ear < EAR_THRESH:
			COUNTER += 1

			# If EAR < Threshold for many consecutive frames trigger alert
			if COUNTER >= EAR_CONSEC_FRAMES:
				if alert_status == False:
					alert_status = True
					# Alert Child Thread
					t = Thread(target=alert, args=('Wake Up',))
					t.deamon = True
					t.start()

				# Display Alert on Screen
				cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		else:
			COUNTER = 0
			alert_status = False

		# Check Yawning Threshold and trigger alert
		if distance > YAWN_THRESH:
			# Display Alert on Screen
			cv2.putText(frame, "Yawn Alert!", (10, 30), 
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			if alert_status2 == False and saying == False:
				alert_status2 = True
				# Alert Child Thread
				t = Thread(target=alert, args=('Yawn Alert. Get some fresh air',))
				t.deamon = True
				t.start()
		else:
			alert_status2 = False

		# Display EAR and YAWN Distance Metric
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), 
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "YAWN: {:.2f}".format(distance), (300, 60), 
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

	# Display Frames with details
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# Termination
	if key == ord("q"):
		break

# Close Stream and Destroy All Windows
cv2.destroyAllWindows()
vs.stop()












