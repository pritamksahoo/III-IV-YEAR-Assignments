import cv2 as cv
import numpy as np
import imutils

path = "/home/pks/Downloads/Assignment/IVP/mini project/"

def orientation(image):
    '''
    Rotate the image before any operation
    based on the pos. of roll no. box w.r.t number table
    '''
    row, col = image.shape[:2]
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

    C1, C2 = min(col, row), max(col, row)

    x,y = 600, 800
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
                # temp_lines.append(np.median(temp, axis=0))
            
        else:
            temp_lines.append(temp[len(temp)//2])
            # temp_lines.append(np.median(temp, axis=0))
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
    image = orientation(image.copy())
    image = cv.resize(image.copy(), (600, 800))

    cv.imshow("org", image)
    cv.waitKey(0)

    # Convert to gray image
    gr_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Thresholding
    thresh = cv.Canny(gr_image, 40, 120)
    # Closing
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2, 3))
    thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)

    row, col = image.shape[:2]
    
    cv.imshow("thresh", thresh)
    cv.waitKey(0)
    
    # ROI Detection <--start-->
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv.contourArea)
    cnt = [list(el[0]) for el in c]

    '''Removing some araeas not needed'''
    b_r = max(cnt, key=lambda x: x[0]+x[1])
    b_l = min(cnt, key=lambda x: x[0]-x[1])

    b_r[1] = b_r[1] - 35
    b_l[1] = b_l[1] - 35
    
    m = (b_l[1]-b_r[1]) / (b_l[0]-b_r[0])
    a, b, c = 1, (-1)*m, m*b_l[0] - b_l[1]
    
    org_sign = a*0 + b*0 + c
    thresh_r = np.array([np.array([(a*i + b*j + c) for j in range(col)]) for i in range(row)])

    if org_sign > 0:
        thresh[thresh_r < 0] = 0
    else:
        thresh[thresh_r > 0] = 0

    '''END'''

    '''Contour detection for extract the ROI'''
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv.contourArea)

    cnt = [list(el[0]) for el in c]

    '''Four corners ofthe ROI'''
    b_r = max(cnt, key=lambda x: x[0]+x[1])
    t_l = min(cnt, key=lambda x: x[0]+x[1])
    t_r = max(cnt, key=lambda x: x[0]-x[1])
    b_l = min(cnt, key=lambda x: x[0]-x[1])

    b_r[0], b_r[1] = b_r[0] + 2, b_r[1] + 0
    b_l[0], b_l[1] = b_l[0] - 2, b_l[1] + 0
    t_r[0], t_r[1] = t_r[0] + 2, t_r[1] - 2
    t_l[0], t_l[1] = t_l[0] - 2, t_l[1] - 2
    
    '''Extract only the ROI'''
    w,h = 800, 600
    # pts1 = np.float32(crop)
    pts1 = np.float32([t_l, t_r, b_l, b_r])
    # w,h = image.shape
    pts2 = np.float32([[0,0], [h,0], [0,w], [h,w]])
    M = cv.getPerspectiveTransform(pts1,pts2)
    image = cv.warpPerspective(image,M,(h,w))
    # ROI Detection <--end-->
    
    cv.imshow("org", image)
    cv.waitKey(0)
    
    gr_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # TODO : Canny edge detection parameters
    edges = cv.Canny(gr_image, 45, 90)
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

    if len(h_lines) >= 14:
        start = 1
    else:
        start = 0

    for i in range(start,len(h_lines)-1):
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