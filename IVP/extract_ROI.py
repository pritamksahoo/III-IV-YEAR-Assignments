import cv2 as cv
import numpy as np
import imutils

path = "/home/pks/Downloads/Assignment/IVP/mini project/"

def orientation(image):
    '''
    Rotate the image before any operation
    based on the pos. of roll no. box w.r.t number table
    '''
    row, col = image.shape
    thresh = cv.Canny(image, 40, 90)
    thresh = cv.dilate(thresh, None, iterations=1)
     
    '''Find max (Number table) and 2nd max (Roll no. box) contour'''
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=lambda x: cv.contourArea(x), reverse=True)
    c1, c2 = cnts[:2]

    rect1, rect2 = cv.minAreaRect(c1), cv.minAreaRect(c2)
    box1, box2 = cv.boxPoints(rect1), cv.boxPoints(rect2)

    # Max
    box1 = sorted(box1, key=lambda x: x[0])
    r_most1, l_most1 = box1[-1], box1[0]

    # 2nd Max
    box2 = sorted(box2, key=lambda x: x[0])
    r_most2, l_most2 = box2[-1], box2[0]

    x,y = 450, 600
    pts1 = np.float32([[0,row], [0,0], [col,row], [col,0]])

    '''Roll no box is at right of number table, rotate left'''
    if l_most2[0] >= r_most1[0]:
        pts2 = np.float32([[x,y], [0,y], [x,0], [0,0]])

    elif r_most2[0] <= l_most1[0]:
        '''Opposite, rotate right'''
        pts2 = np.float32([[0,0], [x,0], [0,y], [x,y]])

    else:
        return image

    M = cv.getPerspectiveTransform(pts1,pts2)
    image = cv.warpPerspective(image,M,(x,y))

    return image
    '''END'''


def intersection_bw_2_lines(l1, l2):
    '''
    Returns point of intersection between 2 lines
    Parameters:
        l1 : line1
        l2 : line2
    Returns:
        x and y coordinate of point of intersection of l1 and l2
    '''
    rho1, theta1 = l1
    rho2, theta2 = l2
    
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    B = np.array([[rho1], [rho2]])
    
    x0, y0 = np.linalg.solve(A, B)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    
    return [x0, y0]

def remove_mult_lines(set_of_lines, dist):
    '''
    Replaces all close lines within some threshold distance with a single one
    Parameters:
        set_of_lines : rho, theta value of all the lines
        dist         : maximum allowed distance b/w two seperate lines
    Returns:
        Well-seperated set of lines (in rho, theta form)
    '''
    
    temp, temp_lines = [], []
    set_of_lines = sorted(set_of_lines, key=lambda x: (abs(x[0]), x[1]))
    
    temp.append(set_of_lines[0])
    for index,point in enumerate(set_of_lines):
        if abs(abs(point[0])-abs(temp[-1][0])) <= dist:
            temp.append(point)
            
            if index == len(set_of_lines)-1:
                temp_lines.append(temp[len(temp)//2])
            
        else:
            temp_lines.append(temp[len(temp)//2])
            temp = [point]
            
            if index == len(set_of_lines)-1:
                temp_lines.append(point)
                
    return temp_lines

    
def extract_roi(image):
    '''
    Extract the marks-table from the image and divide it into cells
    Parametrs:
        image : Given image
    Returns:
        extracted table and four points of each rectangular cell
    '''
    image = orientation(image)
    # row, col = image.shape
    # if row < col:
    #     x,y = 450, 600
    #     pts1 = np.float32([[0,row], [0,0], [col,row], [col,0]])
    #     # w,h = image.shape
    #     pts2 = np.float32([[0,0], [x,0], [0,y], [x,y]])
    #     M = cv.getPerspectiveTransform(pts1,pts2)
    #     image = cv.warpPerspective(image,M,(x,y))
#         image = cv.resize(image, (450, 600))
        
#     image = image[:image.shape[0]-150, :]
    cv.imshow("org", image)
    cv.waitKey(0)
    
    # Thresholding
#     ret, thresh = cv.threshold(image, 115, 255, cv.THRESH_BINARY_INV)
    thresh = cv.Canny(image, 40, 90)
    thresh = cv.dilate(thresh, None, iterations=1)
    thresh[image.shape[0]-150:, :] = 0
    cv.imshow("thresh", thresh)
    cv.waitKey(0)
    
    # ROI Detection <--start-->
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv.contourArea)

    rect = cv.minAreaRect(c)
    box = cv.boxPoints(rect)
    box = np.int0(box)
    box = sorted(box, key=lambda x: x[1])
    p12 = sorted(box[:2].copy(), key=lambda x: x[0])
    p34 = sorted(box[2:].copy(), key=lambda x: x[0])
    crop = np.array(p12 + p34)
    crop[crop < 0] = 0
    
    w,h = 600, 450
    pts1 = np.float32(crop)
    # w,h = image.shape
    pts2 = np.float32([[0,0], [h,0], [0,w], [h,w]])
    M = cv.getPerspectiveTransform(pts1,pts2)
    image = cv.warpPerspective(image,M,(h,w))
    # ROI Detection <--end-->
    
    cv.imshow("org", image)
    cv.waitKey(0)
    
    # TODO : Canny edge detection parameters
    edges = cv.Canny(image, 45, 90)
    cv.imshow("edges", edges)
    cv.waitKey(0)
    
    # Hough Line Detection
    lines = cv.HoughLines(edges,1,np.pi/180,150)
    
    # Removing multiple ambiguous Lines <--start-->
    points = np.array([[line[0][0], line[0][1]] for line in lines])
    pi_val = np.pi
    
    v1 = list(filter(lambda x: x[1]>=0 and x[1]<pi_val/4, points))
    v2 = list(filter(lambda x: x[1]>=(3*pi_val)/4 and x[1]<(5*pi_val)/4, points))
    v3 = list(filter(lambda x: x[1]>=(7*pi_val)/4 and x[1]<=pi_val*2, points))
    
    vertical = v1 + v2 + v3
    
    h1 = list(filter(lambda x: x[1]>=pi_val/4 and x[1]<(3*pi_val)/4, points))
    h2 = list(filter(lambda x: x[1]>=(5*pi_val)/4 and x[1]<(7*pi_val)/4, points))
    
    horizontal = h1 + h2
    
    h_lines = remove_mult_lines(horizontal, 15)
    v_lines = remove_mult_lines(vertical, 15)
    
    lines = h_lines + v_lines
    # # Removing multiple ambiguous Lines <--end-->
    
    # Drawing the lines
    line_image = image.copy()
    for rho, theta in lines:
        # rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        
        cv.line(line_image,(x1,y1),(x2,y2),(0,0,255),1)
    
    cv.imshow("lines", line_image)
    cv.waitKey(0)
    
    ret_cell = []
    
    # Detecting cells
    counter = 1
    for i in range(1,len(h_lines)-1):
        for j in range(1,len(v_lines)-1):
            hl1, hl2 = h_lines[i], h_lines[i+1]
            vl1, vl2 = v_lines[j], v_lines[j+1]
            
            p1 = intersection_bw_2_lines(hl1, vl1)
            p2 = intersection_bw_2_lines(hl1, vl2)
            p3 = intersection_bw_2_lines(hl2, vl1)
            p4 = intersection_bw_2_lines(hl2, vl2)
            
            ret_cell.append([p1, p2, p3, p4])

            # cell = image[p1[1]:p3[1]+1, p1[0]:p2[0]+1]
            
            # cv.imwrite(path + "img" + str(counter) + ".jpg", cell)
            # counter = counter + 1
    
    cv.destroyAllWindows()
    
    return image, ret_cell