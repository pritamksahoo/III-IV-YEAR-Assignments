import cv2 as cv
import numpy as np
import imutils
from keras.models import load_model

from extract_ROI import *
from number_extraction import *
from number_detection import *

path = "/home/pks/Downloads/Assignment/IVP/mini project/"

if __name__ == '__main__':
    image = cv.imread(path+"sample8.jpg", 0)
    model = load_model('apna_model.h5')
    
    roi, cells = extract_roi(image)
    counter, count, row = 1, 0, 0
    for cell in cells:
        if row <= 10:
            if row == 10 and count != 5:
                count = count + 1
                continue

            p1, p2, p3, p4 = cell
            cell_image = roi[p1[1]:p3[1]+1, p1[0]:p2[0]+1]

            cv.imwrite(path + "img.jpg", cell_image)

            image = cv.imread(path+"img.jpg", 0)

            
            conts, number = extract_num(image)
            num, isFraction, divideBy = 0.0, False, 10
            
            if len(conts) != 0:
                conts = sorted(conts, key=lambda x: (x[0], x[1]))
                for r in conts:
                    temp = number[r[0][1]:r[1][1], r[0][0]:r[1][0]]

                    # cv.imshow("temp", temp)
                    # cv.waitKey(0)
                    
                    # cv.imwrite(path + "test" + str(counter) + ".jpg", temp)
                    # counter = counter + 1

                    digit = prediction(temp, model)

                    if digit == 'decimal':
                        isFraction = True

                    else:
                        if isFraction == False:
                            num = num*10.0 + digit
                        else:
                            num = num + (digit / divideBy)
                            divideBy = divideBy * 10

                if row == 10:
                    print("%41.2f" % num)
                else:
                    print("%6.2f" % num, end=' ')

            else:
                print("%6d" % 0, end=' ')

            count = count + 1
            if count == 6:
                print()
                count = 0
                row = row + 1

        else:
            pass