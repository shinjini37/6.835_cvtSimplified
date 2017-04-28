import math

def get_angle(line):
    '''
    returns an angle between 90 and -90
    '''
    x1,y1,x2,y2 = line[0]
    if (x1 == x2):
        return 90
    angle = math.degrees(math.atan((y1-y2)/float(x1-x2)))
        
    return angle

def get_angle_diff(line1, line2):
    angle1 = get_angle(line1)
    angle2 = get_angle(line2)
    diff = abs(angle1-angle2)
##    print "diff", diff
    if diff>90:
        diff = 180 - diff

    return diff

def get_line_equation(line):
    x1,y1,x2,y2 = line[0]
    if (x1-x2==0):
        return (float('inf'), None)
    
    m = (y1-y2)/float(x1-x2)
    c = y1 - m*x1

    return (m, c)

def dist_from_point_to_line(point, line):
    line_params = get_line_equation(line)
    # line params = [m, c, boundaries]
    m, c = line_params
##    print "m", m, "c", c
    if c is None:
        special_x = line[0][0]
        dist = abs(point[0]- special_x)
        return dist, [special_x, point[1]]
    adjusted_point = [point[0], point[1]-c]
    point_length = get_dist([0,0], adjusted_point)
    point_angle = get_angle([[0,0,adjusted_point[0], adjusted_point[1]]])
    m_angle = get_angle([[0, 0, 1, m]])
    diff = abs(m_angle-point_angle)
##    print "angle diff", diff
    dist = point_length*math.sin(math.radians(diff))
    intersect_length = point_length*math.cos(math.radians(diff))
    intersect_x = intersect_length*math.cos(math.radians(m_angle))
    intersect_y = intersect_length*math.sin(math.radians(m_angle))+c

##    print line
##    print point
##    print adjusted_point
##    print point_length
##    print 'point angle', point_angle
##    print 'm angle', m_angle
##    print 'diff', diff
##    print dist
##    print intersect_length
    return (dist, [intersect_x, intersect_y])

def check_point_within_line_segment(point, line):
    endpoint1, endpoint2 = get_endpoints(line)
    length = get_dist(endpoint1, endpoint2)
    midpoint = get_midpoint(line)
    dist, intersect = dist_from_point_to_line(point, line)

    dist1 = get_dist(endpoint1, intersect)
    dist2 = get_dist(endpoint2, intersect)

    # since intersect is on the line, must have both
    # distances be less than length
    if (dist1<=length) and (dist2<=length):
        return True
    return False

def dist_from_point_to_line_segment(point, line):
    line_params = get_line_equation(line)
    endpoint1, endpoint2 = get_endpoints(line)
    dist, intersect = dist_from_point_to_line(point, line)
##    print dist, intersect
    
    m, c = line_params
    if not check_point_within_line_segment(point, line):
        dist1 = get_dist(endpoint1, point)
        dist2 = get_dist(point, endpoint2)
        if (dist1<dist2):
            dist = dist1
            intersect = endpoint1
        else:
            dist = dist2
            intersect = endpoint2

    return dist, intersect

def get_lines_intersect(line1, line2, check_boundaries = False):
    m1, c1 = get_line_equation(line1)
    m2, c2 = get_line_equation(line2)

    if (c1 is None) and (c2 is None): # parallel special case
        return None

    if (m1 == m2): #parallel
        return None

    if (c1 is None):
        x = line1[0][0]
        y = m2*x + c2

    elif (c2 is None):
        x = line2[0][0]
        y = m1*x + c1

    else:
        x = (c2 - c1)/(m1 - m2)
        y = m1*x + c1

    point = [x,y]
    if check_boundaries:
        both_within = True
        for line in [line1, line2]:
            if not check_point_within_line_segment(point, line):
                both_within = False
        if not both_within:
            return None
            
    return (x,y)
    
def get_min_dist_line_segments(line1, line2):
    if get_lines_intersect(line1, line2, check_boundaries = True) is not None:
        return 0
    min_dist = float('inf')
    endpoints1 = get_endpoints(line1)
    endpoints2 = get_endpoints(line2)

    for point in endpoints1:
        dist, intersect = dist_from_point_to_line_segment(point, line2)
##        print point, line2
##        print dist, intersect
        if (dist<min_dist):
            min_dist = dist

    
    for point in endpoints2:
        dist, intersect = dist_from_point_to_line_segment(point, line1)
##        print point, line1
##        print dist, intersect
        
        if (dist<min_dist):
            min_dist = dist
    
    return min_dist

    
def get_dist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.pow(math.pow((x1-x2), 2) + math.pow((y1-y2), 2), .5)

def get_endpoints(line):
    x1,y1,x2,y2 = line[0]
    return ([x1, y1], [x2, y2])

def get_midpoint(line):
    x1,y1,x2,y2 = line[0]
    return [(x1+x2)/2.0, (y1+y2)/2.0]

##def get_min_endpoints_dist(line1,line2):
##    # from line1 to line2
##    min_dist = float('inf')
##    x11,y11,x12,y12 = line1[0]
##    mid1 = get_midpoint(line1)
##
##    points1 = [[x11,y11], [x12,y12], mid1]
##    
##    x21,y21,x22,y22 = line2[0]
##    mid2 = get_midpoint(line2)
##
##    points2 = [[x21,y21], [x22,y22], mid2]
##
##    for point1 in points1:
##        for point2 in points2:
##            dist = get_dist(point1, point2)
##            if dist<min_dist:
##                min_dist = dist
##                            
##    return min_dist

height = 450
width = 600

orig_corners = [[0,0], [width, 0], [width, height], [0, height]]
test_lines = [[[405, 495, 405,  72]],
 [[406, 491, 406,  90]],
 [[ 68, 489, 401, 500]],
 [[404, 497, 404, 250]],
 [[ 59, 407,  71,  68]],
 [[ 78,  61, 351,  61]],
 [[403, 498, 403, 293]],
 [[ 76,  62, 368,  62]],
 [[ 59, 378,  67, 130]],
 [[123, 493, 395, 502]],
 [[407, 335, 407, 119]],
 [[ 60, 426,  63, 320]],
 [[ 66, 488, 205, 492]],
 [[294,  63, 398,  63]],
 [[347, 500, 399, 501]],
 [[133,  60, 336,  60]],
 [[ 61, 446,  63, 361]],
 [[ 67, 221,  72, 108]],
 [[231, 498, 369, 502]],
 [[319,  64, 400,  64]]]

test_lines = [[[405, 495, 405, 72]], [[406, 491, 406, 90]], [[401, 500, 66, 488]], [[404, 497, 404, 250]], [[59, 407, 71, 68]], [[78, 61, 351, 61]], [[403, 498, 403, 293]], [[76, 62, 368, 62]], [[59, 378, 67, 130]], [[123, 493, 395, 502]], [[407, 335, 407, 119]], [[60, 426, 63, 320]], [[294, 63, 398, 63]], [[347, 500, 399, 501]], [[133, 60, 336, 60]], [[61, 446, 63, 361]], [[67, 221, 72, 108]], [[231, 498, 369, 502]], [[319, 64, 400, 64]]]

test_lines = [[[269, 414, 581, 409]], [[15, 416, 472, 409]], [[18, 418, 541, 409]], [[568, 320, 590, 404]], [[161, 52, 495, 69]], [[501, 68, 555, 285]], [[441, 412, 492, 412]], [[503, 70, 572, 347]], [[170, 51, 303, 58]], [[548, 242, 567, 321]], [[52, 196, 63, 141]], [[6, 409, 41, 256]], [[386, 413, 442, 413]], [[269, 60, 437, 68]], [[4, 407, 23, 325]], [[21, 349, 56, 195]], [[390, 63, 499, 66]], [[522, 140, 534, 191]], [[5, 408, 36, 274]], [[439, 66, 500, 68]]]

##for line in test_lines:
##    print line
##    print dist_from_point_to_line_segment(orig_corners[0], line)

##print dist_from_point_to_line_segment(orig_corners[0], test_lines[5])

line = [[6, 409, 41, 256]]
corner = [600, 450]

##print dist_from_point_to_line_segment(corner, line)


line1 = [[256, 109, 264, 109]]
line2 = [[491, 119, 500, 119]]

line1 = [[0, 300, 599, 313]]
line2 = [[157, 299, 161, 299]]

point = [157, 299]

line1 = [[0,0, 1, 1000]]
point = [1,1]

##print get_min_dist_line_segments(line1, line2)
##print dist_from_point_to_line(point, line1)



