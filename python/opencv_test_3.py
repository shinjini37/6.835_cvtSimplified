import cv2
import numpy as np
##from matplotlib import pyplot as plt


def get_edges(img):
    edges = cv2.Canny(img.copy(),100,200)
    edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
    return edges

def get_circles(img):
    circle_img = img.copy()
    circle_img = cv2.cvtColor(circle_img,cv2.COLOR_GRAY2BGR)
    cimg = cv2.medianBlur(img,5)


    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)

    if (circles is not None):
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(circle_img,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(circle_img,(i[0],i[1]),2,(0,0,255),3)

    return circle_img

def write_result(img, result):
    cv2.imwrite('public/images/image.png', img)
    cv2.imwrite('public/images/test.png', result)
    
def shrink_to_size(img):
    height, width = img.shape[:2]
    max_height = min(height, 400)
    max_width = min(width, 400)
    resize = False
    if (height>max_height):
        ratio = float(max_height)/height
        resize = True
    elif (width>max_width):
        ratio = float(max_width)/width
        resize = True
    if (resize):
        img = cv2.resize(img,(int(ratio*width), int(ratio*height)), interpolation = cv2.INTER_AREA)
    return img
    
path = raw_input('path: ')
##execution_type = raw_input('type: ')
##'python/image.png'
img = cv2.imread(path,0)
if (img is not None):
    img = shrink_to_size(cv2.imread(path,0))
    result = get_edges(get_circles(img))
    write_result(img, result)
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

