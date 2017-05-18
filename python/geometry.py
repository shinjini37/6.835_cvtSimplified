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
    m, c = line_params
    if c is None:
        special_x = line[0][0]
        dist = abs(point[0]- special_x)
        return dist, [special_x, point[1]]
    adjusted_point = [point[0], point[1]-c]
    point_length = get_dist([0,0], adjusted_point)
    point_angle = get_angle([[0,0,adjusted_point[0], adjusted_point[1]]])
    m_angle = get_angle([[0, 0, 1, m]])
    diff = abs(m_angle-point_angle)
    dist = point_length*math.sin(math.radians(diff))
    intersect_length = point_length*math.cos(math.radians(diff))
    intersect_x = intersect_length*math.cos(math.radians(m_angle))
    intersect_y = intersect_length*math.sin(math.radians(m_angle))+c

    return (dist, [intersect_x, intersect_y])

def check_point_within_line_segment(point, line):
    endpoint1, endpoint2 = get_endpoints(line)
    length = get_line_length(line)
    dist, intersect = dist_from_point_to_line(point, line)
    
    dist1 = get_dist(endpoint1, point)
    dist2 = get_dist(endpoint2, point)

    # since the point has to be within the line, the dist must be 0
    if dist < 0.0001:
        # since point is within line segment, must have both
        # distances be less than length
        if (dist1<=length) and (dist2<=length):
            return True

    return False

def dist_from_point_to_line_segment(point, line):
    line_params = get_line_equation(line)
    endpoint1, endpoint2 = get_endpoints(line)
    dist, intersect = dist_from_point_to_line(point, line)
    
    m, c = line_params
    if not check_point_within_line_segment(intersect, line):
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

    # this point is on both lines    
    intersect = [x,y]
    
    if check_boundaries:
        both_within = True
        for line in [line1, line2]:
            if not check_point_within_line_segment(intersect, line):
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
        if (dist<min_dist):
            min_dist = dist

    
    for point in endpoints2:
        dist, intersect = dist_from_point_to_line_segment(point, line1)
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

def get_line_length(line):
    x1,y1,x2,y2 = line[0]
    return get_dist([x1,y1],[x2,y2])

def get_midpoint(line):
    x1,y1,x2,y2 = line[0]
    return [(x1+x2)/2.0, (y1+y2)/2.0]



