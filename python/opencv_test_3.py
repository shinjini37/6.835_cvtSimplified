import cv2
import numpy as np
from matplotlib import pyplot as plt
import utility as utils
import circle_processing
import math
import line_merge
import geometry

def get_edges(img):
    edges = cv2.Canny(img,100,200)
##    edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    return edges





def get_circles(img, ref_img = None, help_lines = None):
    if (ref_img is None):
        ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    height, width = img.shape[:2]
    
    cimg = img.copy()
##    inv_img = cv2.bitwise_not(img)    
##    cimg = cv2.medianBlur(img,1)
##    cimg = cv2.GaussianBlur(img,(5,5),0)
    dp = 1
    min_dist = 20
    param1 = 50 # tested value
    param2 = 40 # tested value
    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT, dp, min_dist,
                                param1=param1,param2=param2,minRadius=0,maxRadius=0)
    if (circles is None):
        circles = [[]]
    circles = np.uint16(np.around(circles))
##    for circle in circles[0]:
##        x = circle[0]
##        y = circle[1]
##        r = circle[2]
##        if (r*2 <= height and r*2 <= width):
##            # draw the outer circle
##            cv2.circle(ref_img,(x,y),r,(0,255,0),2)
##            # draw the center of the circle
##            cv2.circle(ref_img,(x,y),2,(0,0,255),3)

    if (help_lines is not None):
        got_circles, cleaned_lines, debug_stuff = circle_processing.get_best_circles(circles, help_lines)


    ##    for circle, got_circle, used_lines in debug_stuff:
    for got_circle in got_circles:
    
##        x = circle[0]
##        y = circle[1]
##        r = circle[2]

        xc = int(got_circle[0])
        yc = int(got_circle[1])
        R = int(got_circle[2])

        
##        # draw the outer circle
##        cv2.circle(img,(x,y),r,(0,255,0),2)
##        # draw the center of the circle
##        cv2.circle(img,(x,y),2,(0,0,255),3)

        # draw the outer circle
        cv2.circle(ref_img,(xc,yc),R,(255,0,255),2)
        # draw the center of the circle
        cv2.circle(ref_img,(xc,yc),3,(0,0,255),3)
        

##        for line in used_lines:
##            for x1,y1,x2,y2 in line:
##                cv2.line(img,(x1,y1),(x2,y2),(0,255,0), 10)

##    for line in help_lines:
##        for x1,y1,x2,y2 in line:
##            cv2.line(ref_img,(x1,y1),(x2,y2),(255,255,0), 1)
##    

    return (ref_img, got_circles, cleaned_lines)





def get_lines(img, ref_img = None, params = None):
    height, width = img.shape[:2]
    
    if params is None:
        minLineLength = 1
        maxLineGap = 1
        threshold = 25 #25
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
        ref_img = cv2.cvtColor(inv_img,cv2.COLOR_GRAY2BGR)
    
##    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
##    edges = cv2.Canny(img,50,150,apertureSize = 3)
##    edges = get_edges(img)
    line_img = ref_img

    blank_image = cv2.bitwise_not(np.zeros((height,width,3), np.uint8))
    
    lines = cv2.HoughLinesP(inv_img,1,np.pi/180,threshold,minLineLength,maxLineGap)

    if (lines is None):
        lines = []
##    print len(lines)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_img,(x1,y1),(x2,y2),(0,255,0), 3)
##            cv2.line(blank_image,(x1,y1),(x2,y2),(0,0,0), 1)
    
    blank_image = cv2.cvtColor(blank_image,cv2.COLOR_BGR2GRAY)

    return (line_img, lines, blank_image)





def get_corners(img, ref_img = None):
    if (ref_img is None):
        ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    corner_img = ref_img
    
    corners = cv2.goodFeaturesToTrack(img,25,0.1,100)
    if (corners is not None):
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

        width1 = geometry.get_dist(corners[0], corners[1])
        width2 = geometry.get_dist(corners[3], corners[2])

        height1 = geometry.get_dist(corners[0], corners[3])
        height2 = geometry.get_dist(corners[1], corners[2])

        av_width = (width1+width2)/2.0
        av_height = (height1+height2)/2.0
        
##        av_width = (abs(corners[1][0]-corners[0][0]) + abs(corners[2][0]-corners[3][0]))/2.0
##        av_height = (abs(corners[3][1]-corners[0][1]) + abs(corners[2][1]-corners[1][1]))/2.0

##        if (av_height>=av_width):
        if max(height1, height2)>=max(width1, width2):            
            corrected_corners = corrected_corners_portrait
            orientation = 'portrait'
        else:
            corrected_corners = corrected_corners_landscape
            orientation = 'landscape'
        return (corrected_corners, orientation)

    corners = order_corners(corners)
    corrected_corners, orientation = get_corrected_corners(corners)
    pts1 = np.float32([corners])
    pts2 = np.float32([corrected_corners])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(corrected_corners[2][0], corrected_corners[2][1]))

    # returns the ordered corners
    return dst, corners, orientation


def get_page_corners(bin_img, img):
    params = { ## tested good values
        "minLineLength": 400000,
        "maxLineGap": 50,
        "threshold": 150,
        "blur": 7
        }

    result, lines, bin_lines = get_lines(bin_img, params = params)
    merged_lines = line_merge.merge_lines(lines)
##    bin_lines = cv2.bitwise_not(bin_lines)

##    params = {
##        "minLineLength": 4,
##        "maxLineGap": 100,
##        "threshold": 50,
##        "blur": None
##        }
##
##    result, lines, bin_lines = get_lines(bin_lines, params = params)
##    
##    print lines
##    def get_angle(line):
##        for x1,y1,x2,y2 in line:
##            angle = math.degrees(math.atan((y1-y2)/float(x1-x2)))%180
##        return angle
##
##    for line in lines:
##        print get_angle(line)
    
##    plt.subplot(121), plt.imshow(img,cmap = 'gray')
##    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
##    plt.subplot(122),plt.imshow(result,cmap = 'gray')
##    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])    
##    plt.show()
####    
    height, width = img.shape[:2]
##    print width, height
##    print merged_lines

    img_corners = [[0,0], [width, 0], [width, height], [0, height]]
    corners = []

    print merged_lines
    
    for img_corner in img_corners:
        min_dist = float('inf')
        best_corner = None
##        print "image corner", img_corner
        for line in merged_lines:
            dist, intersect = geometry.dist_from_point_to_line_segment(img_corner, line)
##            print line
##            print dist, intersect
            if (dist<min_dist):
                min_dist = dist
                best_corner = intersect
        if best_corner is not None:
            corners.append(best_corner)
    
####    
##    max_x = 0
##    max_y = 0
##    min_x = width
##    min_y = height
##    
##    for line in lines:
##        for x1,y1,x2,y2 in line:
##            if x1>max_x:
##                max_x = x1
##            if x2>max_x:
##                max_x = x1
##            if y1>max_y:
##                max_y = y1
##            if y2>max_y:
##                max_y = y2
##
##            if x1<min_x:
##                min_x = x1
##            if x2<min_x:
##                min_x = x2
##            if y1<min_y:
##                min_y = y1
##            if y2<min_y:
##                min_y = y2
##
##    extremes = [min_x, min_y, max_x, max_y]
##    corners = [[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]]
##    print corners
    if len(corners)>0:    
        img, corners, orientation = correct_skew(img, corners)
        bin_img, corners, orientation = correct_skew(bin_img, corners)
    else:
        corners = img_corners
    return bin_img, img, corners


save_pics = True
##save_pics = False

testing = True
testing = False

if not testing:
    path = raw_input()
    corners = raw_input()

else:
    path = 'pic_lib/1.jpg'
    path = 'pic_lib/test_s1.jpg'
    ##path = 'pic_lib/straight1.jpg'
    ##path = 'pic_lib/line_circ.jpg'
    ##path = 'pic_lib/circ.jpg'
    ##path = 'pic_lib/blur_tri.jpg'
    ##path = 'pic_lib/tri.jpg'
    ##path = 'pic_lib/skewed.jpg'
    ##path = 'pic_lib/test1.jpg'
    ##path = 'pic_lib/test2.jpg'
    ##path = 'pic_lib/test3.jpg'

    corners = 'None'

img = cv2.imread(path,0)
if (img is not None):
    img = utils.shrink_to_size(img)
    orig_img = img.copy()

    img_bin = img.copy()
    img_bin = cv2.GaussianBlur(img_bin,(5,5),0)
    img_bin = cv2.adaptiveThreshold(img_bin,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    
    if (corners != 'None'):
        img, corners, orientation = correct_skew(img, eval(corners))
    else:
        bin_img, img, corners = get_page_corners(img_bin, img)

    print corners

    img_bin = img.copy()
    img_bin = cv2.GaussianBlur(img_bin,(5,5),0)
    img_bin = cv2.adaptiveThreshold(img_bin,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

    ref_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    result = ref_img
    
    result, lines, bin_lines = get_lines(img_bin, ref_img = ref_img)



    result, circles, cleaned_lines = get_circles(img_bin, help_lines = lines, ref_img = ref_img)
    merged_lines = line_merge.merge_lines(cleaned_lines)

    return_lines = []
##    merged_lines = cleaned_lines
    for line in merged_lines:
        for x1,y1,x2,y2 in line:
            cv2.line(result,(x1,y1),(x2,y2),(255,255,0), 5)
            return_lines.append([[x1,y1],[x2,y2]])
##    print merged_lines
##    print len(merged_lines)
    
    print return_lines
    print circles

##    result = get_page_corners(img_bin)
##    result = get_corners(img_bin, ref_img = ref_img)
    utils.write_result(result = result, save_copy=save_pics)

##    plt.subplot(121), plt.imshow(orig_img,cmap = 'gray')
##    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
##    plt.subplot(122),plt.imshow(result,cmap = 'gray')
##    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])    
##    plt.show()
##    
######  Or...
####    cv2.imshow('detected circles',result)
####    cv2.waitKey(0)
####    cv2.destroyAllWindows()
##








##    merged_lines = [
####        [[0, 424, 3, 0]],
##        
####        [[291, 29, 82, 236]],
####        [[442, 368, 149, 366]],
####                    [[291, 28, 499, 241]],
####        [[498, 242, 83, 237]],
##        [[397, 0, 549, 1]],
####                    [[146, 238, 147, 368]],
##        [[437, 424, 549, 420]],
####        [[442, 367, 440, 244]],
##        
##                    [[546, 3, 548, 2]],
##        ###### circle segments
####        [[374, 227, 376, 250]],
####        [[251, 154, 263, 148]],
####                    [[321, 320, 352, 298]], [[201, 269, 225, 303]], [[340, 164, 367, 197]],
####                    [[198, 209, 210, 187]], [[206, 190, 243, 155]], [[262, 320, 290, 327]],
####                    [[365, 281, 336, 312]], [[369, 274, 375, 243]], [[369, 201, 376, 236]],
####                    [[340, 165, 302, 147]], [[4, 1, 51, 0]], [[195, 225, 202, 203]],
####                    [[232, 309, 269, 324]], [[196, 253, 206, 275]], [[291, 326, 324, 317]],
####                    [[379, 367, 383, 368]], [[363, 282, 369, 267]], [[199, 259, 195, 239]],
####                    [[262, 149, 296, 146]], [[238, 311, 219, 294]], [[276, 145, 286, 146]],
####                    [[226, 167, 230, 164]], [[197, 216, 197, 211]], [[243, 156, 254, 152]],
####                    [[292, 148, 297, 148]], [[363, 193, 367, 203]], [[309, 321, 311, 321]],
####                    [[362, 188, 339, 165]], [[276, 323, 282, 323]]
##        ]
