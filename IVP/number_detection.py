import cv2 
import os
import numpy as np 
from numpy import loadtxt
from keras.callbacks import EarlyStopping
from keras.models import load_model

early_stopping_monitor = EarlyStopping(patience=3)

path = "/home/pks/Downloads/Assignment/IVP/mini project/"

def resize_image(img, size=(28,28)):
	_,img=cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	#img=cv2.bitwise_not(img)
	# cv2.imshow('image1', img)
	# cv2.waitKey(0)
	#img=cv2.dilate(img,None,iterations=2)
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
	row, col = img.shape
	# print(row*col)

	if (row*col < 25):
		return True
	else:
		return False

def prediction(img, model):
	flag = decimal_check(img)

	if flag == True:
		return 'decimal'
	else:
		#Predicting
		img = resize_image(img)
		# print(img.shape)
		#print(img_inv.shape)


		# Output img with window name as 'image' 
		# cv2.imshow('image', img)
		# cv2.waitKey(0)         
		# cv2.destroyAllWindows() 

		op = model.predict([img.reshape(1,28,28,1)])
		num = np.argmax(op)

		return num

if __name__ == '__main__':
	img = cv2.imread(path+"img43.jpg", 0)
	model = load_model('apna_model.h5')
	prediction(img, model)