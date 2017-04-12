import cv2

def to_JSON_string(obj):
    string = ""
    if isinstance(obj, dict):
        keys = obj.keys()
        for i in xrange(len(keys)):
            key = keys[i]
            key_string = "{\""+str(key)+"\":"+to_JSON_string(obj[key])+"}"
            if i == 0:
                string = key_string
            else:
                string = string+','+key_string
    else:
        if (obj is None):
            string = "\"null\""
        else:
            string = "\""+str(obj)+"\""
    return string


def send(obj):
    print(to_JSON_string(obj))


def write_result(image=None, result=None):
    if (image is not None):
        cv2.imwrite('./public/images/image.png', image)
    if (result is not None):
        cv2.imwrite('./public/images/test.png', result)
    
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
  
