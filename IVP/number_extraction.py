import cv2 as cv
import numpy as np
import imutils
from number_detection import *

path = "/home/pks/Downloads/Assignment/IVP/mini project/"

def approx_rect(con):
    '''
    Determine boundary rectangle of a contour
    Parameters:
        con : Given contour
    Returns:
        Boundary Rectangle
    '''
    
    contours_poly = cv.approxPolyDP(con, 3, True)
    boundRect = cv.boundingRect(contours_poly)
    return boundRect

def all_contour(th):
    '''
    Returns all contour and the particular contours which may contain digit
    '''
    
    cnts = cv.findContours(th.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

#     drawing = image.copy()
    rect = list()
    for c_el in cnts:
        boundRect = approx_rect(c_el)
        area, wh_ratio = boundRect[2]*boundRect[3], boundRect[2]/boundRect[3] 
        top, left = th.shape
        # print(top, left, boundRect)
#         if area > 80 and area < 300 and wh_ratio < 3.5 and wh_ratio > 0.28:
        if 10 <= boundRect[3] <= 25 and 2 <= boundRect[2] <= 25 and 10 < area < 700 and boundRect[0] < left-5 and boundRect[1] > 5:
            rect.append([(int(boundRect[0]), int(boundRect[1])), (int(boundRect[0]+boundRect[2]), int(boundRect[1]+boundRect[3]))])
        
#             cv.rectangle(drawing, (int(boundRect[0]), int(boundRect[1])), (int(boundRect[0]+boundRect[2]), int(boundRect[1]+boundRect[3])), 0, 1)
#     cv.imshow("wrap", drawing)
#     cv.waitKey(0)
        
    return rect, cnts


def isThere(l, el):
    return el in l

def trapped(start, end, rect, w, h):
    '''Remove extra contour pixel created from morphological operation'''
    ret_val = False
    # print("t", start, end, h, w)

    if isThere(start,0) or isThere(end,0) or start[0] == h or start[1] == w or end[0] == h or end[1] == w:
        ret_val = True
        return ret_val

    if [start, end] in rect:
        return ret_val
    
    for point in rect:
        s, e = point

        if (start >= s and end <= e):
            ret_val = True
            break

    return ret_val


def extract_num(image):
    '''
    Extract the part of image where is a valid number
    Parameters:
        image
    Returns:
        Part of the image containing numbers and also boundary rectangle of all the contours within that.
        Each contour signifies some digit or decimal point
    '''
    
#     image = cv.GaussianBlur(image, (3,3), 0)
    row, col = image.shape
    # image = image[2:row-2, 1:col-1]

    # cv.imshow("img", image)
    # cv.waitKey(0)

    _, thresh = cv.threshold(image, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    
    # kernel = np.ones((3,3), np.uint8)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    thresh1 = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

    # cv.imshow("thresh1", thresh1)
    # cv.waitKey(0)

    rect, cnts = all_contour(thresh1)
    if len(rect) == 0:
        rect, cnts = all_contour(thresh)
    
    if len(rect) == 0:
        return [], image
    else:
        left = min(rect, key=lambda x: x[0][0])[0][0]
        right = max(rect, key=lambda x: x[1][0])[1][0]
        top = min(rect, key=lambda x: x[0][1])[0][1]
        bottom = max(rect, key=lambda x: x[1][1])[1][1]
        
        drawing = image.copy()
        ret_val = []
        for c_el in cnts:
            boundRect = approx_rect(c_el)
            start, end = (int(boundRect[0]), int(boundRect[1])), (int(boundRect[0]+boundRect[2]), int(boundRect[1]+boundRect[3]))
            cv.rectangle(drawing, start, end, 0, 1)

            if start[0] > 2 and top <= start[1] and bottom >= end[1] and left <= start[0] and right >= end[0] and not trapped(start, end, rect, row, col):
                ret_val.append([(int(boundRect[0]), int(boundRect[1])), (int(boundRect[0]+boundRect[2]), int(boundRect[1]+boundRect[3]))])

        # cv.imshow("wrap", drawing)
        # cv.waitKey(0)

        return ret_val, image

if __name__ == '__main__':
    
    image = cv.imread(path+"img6.jpg", 0)
    conts, number = extract_num(image)
    print(conts)