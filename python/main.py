import cv2
import numpy as np
from matplotlib import pyplot as plt
import utility as utils
import circle_processing
import line_merge
import geometry

import time


## **** To run manually, comment out "testing = False" and
## put the pathname of the desired file instead
## of "path = 'test_lib/crop_6.jpg'" ****
    
save_pics = True
##save_pics = False

testing = True
testing = False

if not testing:
    path = raw_input()
    corners = raw_input()

else:
    path = 'test_lib/crop_6.jpg'
    corners = 'None'



def get_circles(img, ref_img=None, help_lines=None):
    if ref_img is None:
        ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    height, width = img.shape[:2]
    
    cimg = img.copy()

    dp = 1
    min_dist = 20
    param1 = 50 # tested value
    param2 = 20 # tested value
    
    hough_circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT, dp, min_dist,
                                param1=param1,param2=param2,minRadius=0,maxRadius=0)

    if hough_circles is None:
        hough_circles = [[]]
    hough_circles = np.uint16(np.around(hough_circles))
    circles = hough_circles
        
    if help_lines is not None:
        circles, cleaned_lines, orig_circles = circle_processing.get_best_circles(circles, help_lines)
        
    for got_circle in circles:
        xc = int(got_circle[0])
        yc = int(got_circle[1])
        R = int(got_circle[2])


        # draw the outer circle
        cv2.circle(ref_img,(xc,yc),R,(255,0,255),1)
        # draw the center of the circle
        cv2.circle(ref_img,(xc,yc),3,(0,0,255),2)

    return ref_img, circles, cleaned_lines


def get_lines(img, ref_img = None, params = None):
    height, width = img.shape[:2]
    
    if params is None:
        minLineLength = 1
        maxLineGap = 1
        threshold = 25
        blur = 3
    else:
        minLineLength = params["minLineLength"]
        maxLineGap = params["maxLineGap"]
        threshold = params["threshold"]
        blur = params["blur"]

    inv_img = cv2.bitwise_not(img)
    if blur is not None:
        inv_img = cv2.medianBlur(inv_img,blur)
    if (ref_img is None):
        ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    
    line_img = ref_img

    blank_image = cv2.bitwise_not(np.zeros((height,width,3), np.uint8))
    
    lines = cv2.HoughLinesP(inv_img,1,np.pi/180,threshold,minLineLength,maxLineGap)

    if (lines is None):
        lines = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_img,(x1,y1),(x2,y2),(0,255,0), 1)
    
    blank_image = cv2.cvtColor(blank_image,cv2.COLOR_BGR2GRAY)
    
    return (line_img, lines, blank_image)


def get_corners(img, ref_img=None):
    if ref_img is None:
        ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    corner_img = ref_img
    
    corners = cv2.goodFeaturesToTrack(img,25,0.1,100)
    if corners is not None:
        corners = np.int0(corners)

        for i in corners:
            x, y = i.ravel()
            cv2.circle(corner_img, (x, y), 3, 255, -1)
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

        width1 = geometry.get_dist(corners[0], corners[1])
        width2 = geometry.get_dist(corners[3], corners[2])

        height1 = geometry.get_dist(corners[0], corners[3])
        height2 = geometry.get_dist(corners[1], corners[2])

        av_width = (width1+width2)/2.0
        av_height = (height1+height2)/2.0
        
        if max(height1, height2)>=max(width1, width2):            
            corrected_corners = corrected_corners_portrait
            orientation = 'portrait'
            edge_lines = [[[0,0,0,550]], [[0,0,425,0]], [[0,550,425,550]], [[425,0,425, 550]]]

        else:
            corrected_corners = corrected_corners_landscape
            orientation = 'landscape'
            edge_lines = [[[0,0,550,0]], [[0,0,0,425]], [[550,0, 550, 425]], [[0, 425, 550, 425]]]

        return corrected_corners, orientation, edge_lines

    corners = order_corners(corners)
    corrected_corners, orientation, edge_lines = get_corrected_corners(corners)
    pts1 = np.float32([corners])
    pts2 = np.float32([corrected_corners])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(corrected_corners[2][0], corrected_corners[2][1]))

    # returns the ordered corners
    return dst, corners, orientation, edge_lines


def get_page_corners(bin_img, img):
    params = { ## tested good values
        "minLineLength": 400000,
        "maxLineGap": 50,
        "threshold": 150,
        "blur": 5
        }

    result, lines, bin_lines = get_lines(bin_img, params = params)
    merged_lines = line_merge.merge_lines(lines)
    height, width = img.shape[:2]

    img_corners = [[0,0], [width, 0], [width, height], [0, height]]
    edge_lines = []#[[[0,0,width, 0]],[[0,0,0,height]],[[width,0,width,height]],[[0,height,width,height]]]
    
    corners = []

    for img_corner in img_corners:
        min_dist = float('inf')
        best_corner = None
        for line in merged_lines:
            if geometry.get_line_length(line)>min(height/8.0, width/8.0):
                dist, intersect = geometry.dist_from_point_to_line_segment(img_corner, line)
                if (dist<min_dist):
                    min_dist = dist
                    best_corner = intersect
        if best_corner is not None:
            if (min_dist>max(height/2.0, width/2.0)): #hackityhack
                corners.append(img_corner)
            else:
                corners.append(best_corner)
    
    if len(corners)==0:    
        corners = img_corners
    
    img, corners, orientation, edge_lines = correct_skew(img, corners)
    bin_img, corners, orientation, edge_lines = correct_skew(bin_img, corners)
        
    return bin_img, img, corners, edge_lines

##
### from http://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
##def rotate_bound(image, angle):
##    # grab the dimensions of the image and then determine the
##    # center
##    (h, w) = image.shape[:2]
##    (cX, cY) = (w // 2, h // 2)
## 
##    # grab the rotation matrix (applying the negative of the
##    # angle to rotate clockwise), then grab the sine and cosine
##    # (i.e., the rotation components of the matrix)
##    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
##    print M
##    cos = np.abs(M[0, 0])
##    sin = np.abs(M[0, 1])
## 
##    # compute the new bounding dimensions of the image
##    nW = int((h * sin) + (w * cos))
##    nH = int((h * cos) + (w * sin))
## 
##    # adjust the rotation matrix to take into account translation
##    M[0, 2] += (nW / 2) - cX
##    M[1, 2] += (nH / 2) - cY
## 
##    # perform the actual rotation and return the image
##    return cv2.warpAffine(image, M, (nW, nH))
##
##def rotate_point(point,image,angle):
##    def apply_m(point, M):        
##        point_inv = [point[1], point[0]]
##
##        point_inv = [
##            point_inv[0]*M[0][0] + point_inv[1]*M[1][0],
##            point_inv[0]*M[0][1] + point_inv[1]*M[1][1]
##            ]
##
##        point = [point_inv[1], point_inv[0]]
####        point = [
####            point[0]*M[0][0] + point[1]*M[1][0],
####            point[0]*M[0][1] + point[1]*M[1][1]
####            ]
##
##
##        return point
##
##    (h, w) = image.shape[:2]
##    center = (w // 2, h // 2)
## 
##    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
##    point[0] = point[0]-center[0]
##    point[1] = point[1]-center[1]
##
##
##    point = apply_m(point, M)
##    [nw,nh] = apply_m(center,M)
##    print center
##    print nw, nh
##    
##    point[0] = point[0] + nw
##    point[1] = point[1] + nh
##    
##    return point    

img = cv2.imread(path,0)
if (img is not None):
    
    start = time.time()
    
    img = utils.shrink_to_size(img)
    orig_img = img.copy()

    img_bin = img.copy()
    img_bin = cv2.GaussianBlur(img_bin,(5,5),0)
    img_bin = cv2.adaptiveThreshold(img_bin,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    edge_lines = []
    if (corners != 'None'):
        img, corners, orientation, edge_lines = correct_skew(img, eval(corners))
    else:
        bin_img, img, corners, edge_lines = get_page_corners(img_bin, img)

    print corners

    img_bin = img.copy()
    img_bin = cv2.GaussianBlur(img_bin,(5,5),0)
    img_bin = cv2.adaptiveThreshold(img_bin,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    result = ref_img
        
    result, lines, bin_lines = get_lines(img_bin, ref_img = None)

    result, circles, cleaned_lines = get_circles(img_bin, help_lines = lines, ref_img = ref_img)
    
    merged_lines = line_merge.merge_lines(cleaned_lines, edge_lines = edge_lines)

    return_lines = []

    for line in merged_lines:
        for x1,y1,x2,y2 in line:
            cv2.line(result,(x1,y1),(x2,y2),(255,255,0), 2)
            return_lines.append([[x1,y1],[x2,y2]])

    print return_lines

    print circles

    end = time.time()

    if not testing:
        utils.write_result(result = result, save_copy=save_pics)
    else:
        print 'num lines: ', len(return_lines)
        print 'num circles: ', len(circles)
        print 'time: ', (end - start)

        plt.subplot(131), plt.imshow(orig_img,cmap = 'gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(132), plt.imshow(img_bin,cmap = 'gray')
        plt.title('Binarized Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(133),plt.imshow(result,cmap = 'gray')
        plt.title('Result Image'), plt.xticks([]), plt.yticks([])    
        plt.show()
    
