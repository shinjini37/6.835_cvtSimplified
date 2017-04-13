import cv2
import numpy as np
from matplotlib import pyplot as plt
import utility as utils


def get_edges(img):
    edges = cv2.Canny(img,100,200)
##    edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    return edges

def get_circles(img, ref_img = None):
    if (ref_img is None):
        ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    height, width = img.shape[:2]
    circle_img = ref_img
    

##    cimg = img.copy()
##    inv_img = cv2.bitwise_not(img)    
    cimg = cv2.medianBlur(img,5)
##    cimg = cv2.GaussianBlur(img,(5,5),0)

    
    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,
                                param1=60,param2=30,minRadius=0,maxRadius=0)
    if (circles is None):
        circles = [[]]
    circles = np.uint16(np.around(circles))
    for circle in circles[0]:
        x = circle[0]
        y = circle[1]
        r = circle[2]
        if (r*2 <= height and r*2 <= width):
            # draw the outer circle
            cv2.circle(circle_img,(x,y),r,(0,255,0),2)
            # draw the center of the circle
            cv2.circle(circle_img,(x,y),2,(0,0,255),3)

    return circle_img

def get_lines(img, ref_img = None):
    if (ref_img is None):
        ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    inv_img = cv2.bitwise_not(img)
##    print img
##    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##    edges = cv2.Canny(img,50,150,apertureSize = 3)
##    edges = get_edges(img)
    line_img = ref_img
    
    minLineLength = 50
    maxLineGap = 10
    lines = cv2.HoughLinesP(inv_img,1,np.pi/180,100,minLineLength,maxLineGap)

    if (lines is None):
        lines = []
        
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_img,(x1,y1),(x2,y2),(0,255,0),2)


##    lines = cv2.HoughLines(edges,1,np.pi/180,200)
   
##    for line in lines:
##        for rho,theta in line:
##            a = np.cos(theta)
##            b = np.sin(theta)
##            x0 = a*rho
##            y0 = b*rho
##            x1 = int(x0 + 1000*(-b))
##            y1 = int(y0 + 1000*(a))
##            x2 = int(x0 - 1000*(-b))
##            y2 = int(y0 - 1000*(a))
##
##            cv2.line(line_img,(x1,y1),(x2,y2),(0,0,255),2)

    return line_img

def get_corners(img, ref_img = None):
    if (ref_img is None):
        ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    corner_img = ref_img
    
    corners = cv2.goodFeaturesToTrack(img,25,0.1,100)
    corners = np.int0(corners)

    for i in corners:
        x,y = i.ravel()
        cv2.circle(corner_img,(x,y),3,255,-1)
    return corner_img

def correct_skew(img, corners):

    def order_corners(corners):
    # for 4 corners!

        def sort_by(corners, sort_type):
            def compare(a,b):
                if a[sort_type]-b[sort_type]>0:
                    return 1
                if a[sort_type]-b[sort_type]<0:
                    return -1
                return 0
            return sorted(corners, compare)
        
        if len(corners) != 4:
            raise RuntimeError("The number of corners has to be 4")
        lefts = []
        rights = []
        x_sorted = sort_by(corners, 0)
        for i in xrange(4):
            if i<2:
                lefts.append(x_sorted[i])
            else:
                rights.append(x_sorted[i])

        left_y_sorted = sort_by(lefts, 1)
        right_y_sorted = sort_by(rights, 1)

        top_left = left_y_sorted[0]
        bottom_left = left_y_sorted[1]

        top_right = right_y_sorted[0]
        bottom_right = right_y_sorted[1]

        return [top_left, top_right, bottom_right, bottom_left]
            
        

    def get_corrected_corners(corners):
        corrected_corners_portrait = [[0,0], [425, 0], [425, 550], [0, 550]]
        corrected_corners_landscape = [[0,0], [550, 0], [550, 425], [0, 425]]

        av_width = (abs(corners[1][0]-corners[0][0]) + abs(corners[2][0]-corners[3][0]))/2.0
        av_height = (abs(corners[3][1]-corners[0][1]) + abs(corners[2][1]-corners[1][1]))/2.0

        if (av_height>=av_width):
            corrected_corners = corrected_corners_portrait
            orientation = 'portrait'
        else:
            corrected_corners = corrected_corners_landscape
            orientation = 'landscape'
        return (corrected_corners, orientation)

    corners = order_corners(corners)
    corrected_corners, orientation = get_corrected_corners(corners)
    print(corrected_corners, orientation)
    pts1 = np.float32([corners])
    pts2 = np.float32([corrected_corners])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(corrected_corners[2][0], corrected_corners[2][1]))

    return dst
  
path = raw_input('path: ')
corners = raw_input('corners: ')


##path = 'line_circ.jpg'
##path = 'circ.jpg'

##execution_type = raw_input('type: ')
##'python/image.png'
img = cv2.imread(path,0)
if (img is not None):
    img = utils.shrink_to_size(img)
    if (corners != 'None'):
        print ('corners are ', corners)
        img = correct_skew(img, eval(corners))

    ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    
    img_bin = img.copy()
##    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
##    result = clahe.apply(img)
##    result = cv2.medianBlur(result,5)
    img_bin = cv2.GaussianBlur(img_bin,(5,5),0)
    img_bin = cv2.adaptiveThreshold(img_bin,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
####    result = get_edges(get_circles(result))
    result = get_circles(img_bin, ref_img = ref_img)
    result = get_lines(img_bin, ref_img = ref_img)
    result = get_corners(img_bin, ref_img = ref_img)
    utils.write_result(result = result)
##
##    plt.subplot(121),plt.imshow(img,cmap = 'gray')
##    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
##    plt.subplot(122),plt.imshow(result,cmap = 'gray')
##    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
##    
##    plt.show()
####  Or...
##    cv2.imshow('detected circles',result)
##    cv2.waitKey(0)
##    cv2.destroyAllWindows()

