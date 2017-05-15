import general_merge
import geometry

def get_max_dist_endpoints(line1, line2):
    max_dist = 0
    x11,y11,x12,y12 = line1[0]
    
    
    x21,y21,x22,y22 = line2[0]

    points = [[x11,y11], [x12,y12], [x21,y21], [x22,y22]]
    
    max_point1 = None
    max_point2 = None
    
    for point1 in points:
        for point2 in points:
            dist = geometry.get_dist(point1, point2)
            if dist>max_dist:
                max_dist = dist
                max_point1 = point1
                max_point2 = point2

    return (max_dist, [max_point1, max_point2])

            



def get_merged_line(lines):
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


def check_line_merge_criteria(ref_line, test_line):
    
    angle_thresh = 5
    dist_thresh = 20

    merge = False

    length = geometry.get_dist(test_line[0][:2], test_line[0][2:])
    
    diff = geometry.get_angle_diff(ref_line, test_line)
    if (diff < angle_thresh):
        dist = geometry.get_min_dist_line_segments(ref_line, test_line)
        if (dist<dist_thresh):
            merge = True
    return merge

def check_line_merge_criteria_circ(ref_line, test_line):

    angle_thresh = 1
    dist_thresh = 5

    merge = False

    length = geometry.get_dist(test_line[0][:2], test_line[0][2:])
    
    diff = geometry.get_angle_diff(ref_line, test_line)
    if (diff < angle_thresh):
        dist = geometry.get_min_dist_line_segments(ref_line, test_line)
        if (dist<dist_thresh):
            merge = True
    return merge



def merge_lines(lines, circle = False):
    if circle:
        return general_merge.merge(lines, get_merged_line, check_line_merge_criteria_circ)    
    return general_merge.merge(lines, get_merged_line, check_line_merge_criteria)

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
