import cv2 as cv
import numpy as np
import imutils

from extract_ROI import *
from number_extraction import *
from number_detection import *

path = "/home/pks/Downloads/Assignment/IVP/mini project/"

if __name__ == '__main__':
    image = cv.imread(path+"sample11.jpg", 0)
    
    roi, cells = extract_roi(image)
    counter = 1
    for cell in cells:
        p1, p2, p3, p4 = cell
        cell_image = roi[p1[1]:p3[1]+1, p1[0]:p2[0]+1]

        cv.imwrite(path + "img.jpg", cell_image)

        image = cv.imread(path+"img.jpg", 0)

        
        conts, number = extract_num(image)
        num = 0.0
        
        if len(conts) != 0:
            conts = sorted(conts, key=lambda x: (x[0], x[1]))
            for r in conts:
                temp = number[r[0][1]:r[1][1], r[0][0]:r[1][0]]
                # cv.imshow("temp", temp)
                # cv.waitKey(0)
                
                # cv.imwrite(path + "test" + str(counter) + ".jpg", temp)
                # counter = counter + 1

                digit = detect_digit(temp)