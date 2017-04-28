import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('pic_lib/1.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT()
kp = sift.detect(gray,None)

img=cv2.drawKeypoints(gray,kp)

cv2.imshow('result',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
