import math
import random


def get_angle(line):
    x1,y1,x2,y2 = line[0]
    angle = (math.degrees(math.atan2((y1-y2),(x1-x2)))+360)%180
        
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
    # line params = [m, c, boundaries]
    m, c = line_params
    if c is None:
        special_x = line[0][0]
        dist = point[0]- special_x
        return dist, [special_x, point[1]]
    adjusted_point = [point[0], point[1]-c]
    point_length = get_dist([0,0], adjusted_point)
    point_angle = get_angle([[0,0,adjusted_point[0], adjusted_point[1]]])
    m_angle = get_angle([[0, c, 1, (m+c)]])
    diff = abs(m_angle-point_angle)
    dist = point_length*math.sin(math.radians(diff))
    intersect_length = point_length*math.cos(math.radians(diff))
    intersect_x = intersect_length*math.cos(math.radians(m_angle))
    intersect_y = intersect_length*math.sin(math.radians(m_angle))+c
    
    
    return (dist, [intersect_x, intersect_y])

def check_point_within_line_segment(point, line):
    endpoint1, endpoint2 = get_endpoints(line)
    length = get_dist(endpoint1, endpoint2)
    midpoint = get_midpoint(line)
    dist, intersect = dist_from_point_to_line(point, line)

    dist1 = get_dist(endpoint1, intersect)
    dist2 = get_dist(endpoint2, intersect)
    if min(dist1,dist2)>length/2.0:
        return False
    return True

def dist_from_point_to_line_segment(point, line):
    line_params = get_line_equation(line)
    endpoint1, endpoint2 = get_endpoints(line)
    dist, intersect = dist_from_point_to_line(point, line)
    
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
        dist = dist_from_point_to_line_segment(point, line2)
        if (dist<min_dist):
            min_dist = dist

    
    for point in endpoints2:
        dist = dist_from_point_to_line_segment(point, line1)
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

def get_max_dist_endpoints(line1, line2):
    max_dist = 0
    x11,y11,x12,y12 = line1[0]
    
    
    x21,y21,x22,y22 = line2[0]

    points = [[x11,y11], [x12,y12], [x21,y21], [x22,y22]]
    
    max_point1 = None
    max_point2 = None
    
    for point1 in points:
        for point2 in points:
            dist = get_dist(point1, point2)
            if dist>max_dist:
                max_dist = dist
                max_point1 = point1
                max_point2 = point2

    return (max_dist, [max_point1, max_point2])

            



def get_merged_line(lines):
##    num_lines = len(lines)
##    av_angle = 0
##    length = 0
##    midpoint = [0,0]
##    for line in lines:
##        for x1,y1,x2,y2 in line:
##            av_angle += get_angle(line)
##            point1, point2 = get_endpoints(line)
##            length += get_dist(point1, point2)
##            midpoint = [midpoint[0]+x1+x2, midpoint[1]+y1+y2]
##
##    av_angle = av_angle/float(num_lines)
##    midpoint = [midpoint[0]/(2.0*num_lines), midpoint[1]/(2.0*num_lines)]
##
##    av_angle_rad = math.radians(av_angle)
##    end1 = [midpoint[0] + length*math.cos(av_angle_rad)/2.0,
##            midpoint[0] + length*math.sin(av_angle_rad)/2.0]
##    end2 = [midpoint[0] - length*math.cos(av_angle_rad)/2.0,
##            midpoint[0] - length*math.sin(av_angle_rad)/2.0]
    max_max_dist = 0
    max_max_point1 = None
    max_max_point2 = None
    for line1 in lines:
        for line2 in lines:
            (max_dist, [max_point1, max_point2]) = get_max_dist_endpoints(line1, line2)
            if max_dist>max_max_dist:
                max_max_dist = max_dist
                max_max_point1 = max_point1
                max_max_point2 = max_point2
    
        
##    return [[end1[0], end1[1], end2[0], end2[1]]]
    return [[max_max_point1[0], max_max_point1[1], max_max_point2[0], max_max_point2[1]]]

def merge_lines_helper(lines):
    angle_thresh = 5
    dist_thresh = 15
    
    merged_lines = []

    remaining_lines = lines[:]
    
    seed_idx = 0 #random.choice(range(len(lines)))
    seed_line = lines[seed_idx]
    groups = [[seed_line]]
    to_remove_idxs = [0]
    current_group_idx = 0
    while (len(remaining_lines)>0):
        for i in xrange(1, len(remaining_lines)):
            growing_line = get_merged_line(groups[current_group_idx])
            line = remaining_lines[i]
            diff = get_angle_diff(growing_line, line)
            if (diff < angle_thresh):
##                dist = get_min_endpoints_dist(growing_line, line)
                dist = get_min_dist_line_segments(growing_line, line)
                if (dist<dist_thresh):
                    groups[current_group_idx].append(line)
                    to_remove_idxs.append(i)
        remaining_lines_copy = []
        for i in xrange(len(remaining_lines)):
            if i not in to_remove_idxs:
                remaining_lines_copy.append(remaining_lines[i][:])
        remaining_lines = remaining_lines_copy
##        print groups[current_group_idx]
##        print 'smoll dood', remaining_lines[9]
        if (len(remaining_lines)>0):
            current_group_idx += 1
            next_seed = remaining_lines[0]
            groups.append([next_seed])
            to_remove_idxs = [0]

    for group in groups:
        merged_line = get_merged_line(group)
##        print group
##        for line in group:
##            print get_angle(line)
        print merged_line
        print get_angle(merged_line)
        merged_lines.append(merged_line)
    print len(groups)
    return merged_lines

def merge_lines(lines):
    num_lines = len(lines)
    merged_lines = lines
    done = False
    while not done:
        merged_lines = merge_lines_helper(merged_lines)
        num_merged_lines = len(merged_lines)
        if (num_merged_lines == num_lines):
            done = True
        else:
            num_lines = num_merged_lines

    return merged_lines
        

##test = [[[406, 536, 419, 283]],
##
## [[408, 533, 417, 360]],
##
## [[ 34,  23, 206 , 23]],
##
## [[412, 378, 436,  24]],
##
## [[ 58,  25, 360,  25]],
##
## [[167, 550, 375, 540]],
##
## [[ 46,  24, 360,  24]],
##
## [[ 17, 232,  25, 403]],
##
## [[ 17,  22, 202,  22]],
##
## [[ 17, 223,  26, 387]],
##
## [[427, 174, 438,  24]],
##
## [[  7,  48,  21, 262]],
##
## [[196,  26, 355,  26]]]
##
##merge_lines(test)
##point = [0,2]
##line = [[1,0,2,0]]
##line2 = [[2,1,3,2]]
##
####print dist_from_point_to_line_segment(point, line)
##print get_lines_intersect(line, line2)

##[[269, 414, 581, 409]]
##179.081876998
##[[15, 416, 541, 409]]
##179.237553646
##[[590, 404, 501, 68]]
##75.1641464871
##[[161, 52, 500, 68]]
##2.70222026813
##[[492, 412, 386, 413]]
##179.459489813
##[[63, 141, 21, 349]]
##101.415839524
##[[6, 409, 41, 256]]
##102.8851694
##print get_min_dist_line_segments([[6, 409, 41, 256]], [[63, 141, 21, 349]])
