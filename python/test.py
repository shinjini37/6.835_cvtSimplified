import cv2
import numpy as np
from matplotlib import pyplot as plt
import utility as utils




## 8.5 * 11 = 425, 550

## find major axis

## apply transformation


## for circ.jpg
##corners = [[22.647735595703125, 32.00000762939453], \
##           [285.6477355957031, 49.00000762939453], \
##           [285.6477355957031, 375.00000762939453], \
##           [24.647735595703125, 381.00000762939453]]

## for line_circ.jpg
corners = [[1.647735595703125, 12.000007629394531], \
           [291.6477355957031, 15.000007629394531], \
           [269.6477355957031, 357.00000762939453], \
           [9.647735595703125, 371.00000762939453]]

def correct_skew(img, corners):

    def get_corrected_corners(corners):
        corrected_corners_portrait = [[0,0], [425, 0], [425, 550], [0, 550]]
        corrected_corners_landscape = [[0,0], [550, 0], [550, 425], [0, 425]]

        av_width = ((corners[1][0]-corners[0][0]) + (corners[3][0]-corners[2][0]))/2.0
        av_height = ((corners[3][1]-corners[0][1]) + (corners[2][1]-corners[1][1]))/2.0

        if (av_height>=av_width):
            corrected_corners = corrected_corners_portrait
            orientation = 'portrait'
        else:
            corrected_corners = corrected_corners_landscape
            orientation = 'landscape'
        return (corrected_corners, orientation)

    
    corrected_corners, orientation = get_corrected_corners(corners)
    print(corrected_corners, orientation)
    pts1 = np.float32([corners])
    pts2 = np.float32([corrected_corners])

    M = cv2.getPerspectiveTransform(pts1,pts2)

    dst = cv2.warpPerspective(img,M,(corrected_corners[2][0], corrected_corners[2][1]))

    return dst


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
    print x_sorted
    for i in xrange(4):
        if i<2:
            lefts.append(x_sorted[i])
        else:
            rights.append(x_sorted[i])

    print lefts, rights

    left_y_sorted = sort_by(lefts, 1)
    right_y_sorted = sort_by(rights, 1)

    print left_y_sorted, right_y_sorted

    top_left = left_y_sorted[0]
    bottom_left = left_y_sorted[1]

    top_right = right_y_sorted[0]
    bottom_right = right_y_sorted[1]

    return [top_left, top_right, bottom_right, bottom_left]
##
##img = cv2.imread('line_circ.jpg')
##if (img is not None):
##    img = utils.shrink_to_size(img)
##
##    for corner in corners:
##        x = int(corner[0])
##        y = int(corner[1])
##        cv2.circle(img,(x,y),3,255,-1)
##
##    dst = correct_skew(img, corners)
##
##    plt.subplot(121),plt.imshow(img),plt.title('Input')
##    plt.subplot(122),plt.imshow(dst),plt.title('Output')
##    plt.show()

print(order_corners([[1,1], [1,0], [0,0], [0,1]]))
