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
