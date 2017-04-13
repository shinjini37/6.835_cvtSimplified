import utility as utils
import cv2

path = raw_input()

img = cv2.imread(path,0)
if (img is not None):
    ## ratio might be useful to know
    (img, width, height) = utils.shrink_to_size(img, get_dims  = True)
##    Use utils.send for JSON!
##    utils.send('width,'+str(width))
##    utils.send('height,'+str(height))
    print 'width,'+str(width)
    print 'height,'+str(height)
    utils.write_result(image = img)
