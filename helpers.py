from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np

# Utility Function - Calculate Eye Aspect Ratio(EAR)
def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])

	ear = (A + B) / (2.0 * C)
	return ear

# Utility Function - Calculates EAR of the driver
def getEAR(shape):
	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

	leftEye, rightEye = shape[lStart:lEnd], shape[rStart:rEnd]

	leftEAR, rightEAR = eye_aspect_ratio(leftEye), eye_aspect_ratio(rightEye)

	ear = (leftEAR + rightEAR)/2.0
	return (ear, leftEye, rightEye)

# Utility Function - Calculate Lip Distance
def getLipDist(shape):
	upper_lip = shape[50:53]
	upper_lip = np.concatenate((upper_lip, shape[61:64]))

	lower_lip = shape[56:59]
	lower_lip = np.concatenate((lower_lip, shape[65:68]))

	upper_mean = np.mean(upper_lip, axis = 0)
	lower_mean = np.mean(lower_lip, axis = 0)

	dist = abs(upper_mean[1] - lower_mean[1])

	return dist
