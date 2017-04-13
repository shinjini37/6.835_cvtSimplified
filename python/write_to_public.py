import utility as utils
import cv2

path = raw_input('path: ')

img = cv2.imread(path,0)
if (img is not None):
    img = utils.shrink_to_size(img)
    utils.write_result(image = img)
