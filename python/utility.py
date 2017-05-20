import cv2

from datetime import datetime

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


def write_result(image=None, result=None, save_copy=False):
    if (image is not None):
        cv2.imwrite('./public/images/image.png', image)
    if (result is not None):
        cv2.imwrite('./public/images/result.png', result)
        if save_copy:
            filename = './python/results/'+datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.png'
            cv2.imwrite(filename, result)
        
    
def shrink_to_size(img, get_dims = False):
    height, width = img.shape[:2]
    MAX = 600
    
    max_height = min(height, MAX)
    max_width = min(width, MAX)

    ratio = 1

    if (height>width):
        max_dim = 'height'
    else:
        max_dim = 'width'
    resize = False

    if (max_dim == 'height'):
        if (height>max_height):
            ratio = float(max_height)/height
            resize = True
    else:
        if (width>max_width):
            ratio = float(max_width)/width
            resize = True
    if (resize):
        height = int(ratio*height)
        width = int(ratio*width)
        img = cv2.resize(img,(width, height), interpolation = cv2.INTER_AREA)
    if get_dims:
        return (img, width, height)
    return img

