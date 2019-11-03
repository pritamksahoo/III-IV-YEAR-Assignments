import cv2 
import os
import numpy as np 
from numpy import loadtxt
from keras.callbacks import EarlyStopping
from keras.models import load_model

early_stopping_monitor = EarlyStopping(patience=3)

path = "/home/pks/Downloads/Assignment/IVP/mini project/"

def resize_image(img, size=(28,28)):
	'''
	Resizing image into 28x28 pixels according to MNIST Standard
	'''
	_, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	# cv2.imshow('image1', img) 
	# cv2.waitKey(0)

	h, w = img.shape[:2]

	if h == w: 
		return cv2.resize(img, size, cv2.INTER_AREA)

	if h > w:
		dif = h
	else:
		dif = w 

	if dif > (size[0]+size[1])//2 :
		interpolation = cv2.INTER_AREA

	else :
		interpolation =cv2.INTER_CUBIC

	x_pos = (dif - w)//2
	y_pos = (dif - h)//2

	if len(img.shape) == 2:
		mask = np.zeros((dif, dif), dtype=img.dtype)
		mask[y_pos:y_pos+h, x_pos:x_pos+w] = img[:h, :w]
	else:
		mask = np.zeros((dif, dif, c), dtype=img.dtype)
		mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = img[:h, :w, :]

	return cv2.resize(mask, size, interpolation) 


def decimal_check(img):
	'''
	Check if img is decimal point or not
	'''
	row, col = img.shape
	# print(row*col)

	if (row*col < 25):
		return True
	else:
		return False


def one_check(img):
	'''Check if img is obvious 1'''
	h, w = img.shape
	wh_ratio = h/w

	if wh_ratio >= 5:
		return True

	else:
		return False


def prediction(img, model):
	'''
	Digit Prediction
	'''
	d_flag = decimal_check(img)
	one_flag = one_check(img)

	if d_flag == True:
		return 'decimal'
	elif one_flag == True:
		return 1
	else:
		#Predicting
		img = resize_image(img)
		# Output img with window name as 'image' 
		# cv2.imshow('image', img)
		# cv2.waitKey(0)         
		# cv2.destroyAllWindows() 

		op = model.predict([img.reshape(1,28,28,1)])
		num = np.argmax(op)

		return num

if __name__ == '__main__':
	img = cv2.imread(path+"img7.jpg", 0)
	model = load_model('apna_model.h5')

	print(prediction(img, model))
