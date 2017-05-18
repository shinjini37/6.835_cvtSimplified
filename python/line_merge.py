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
    
    return [[max_max_point1[0], max_max_point1[1], max_max_point2[0], max_max_point2[1]]]

def make_check_line_merge_criteria(circle=False):
    if circle:
        angle_low_thresh = .1
        angle_high_thresh = .1
        length_high_thresh = 75
        dist_thresh = 1

        min_length = 0
        min_length_dist = 0
        
    else:        
        angle_low_thresh = 2#1
        angle_high_thresh = 7
        length_high_thresh = 75
        dist_thresh = 5

        min_length = 5
        min_length_dist = 2
                
    def check_line_merge_criteria(ref_line, test_line):
        

        merge = False

        test_line_length = geometry.get_line_length(test_line)
        dist = geometry.get_min_dist_line_segments(ref_line, test_line)
        diff = geometry.get_angle_diff(ref_line, test_line)

     ## this generally causes bad merges and results in directions changing easily   
##        if test_line_length<min_length:
##            if dist<min_length_dist:
##                merge = True
                
        if (dist<dist_thresh):
            if (test_line_length>length_high_thresh):
                if (diff < angle_low_thresh):
                    merge = True
            else:
                if (diff < angle_high_thresh):
                    merge = True
        return merge

    return check_line_merge_criteria

def clean_merge_lines(merge_lines, edge_lines):
    cleaned_lines = []
    for line in merge_lines:
        if not clean_merge_line(line, edge_lines):
            cleaned_lines.append(line)
    return cleaned_lines

def clean_merge_line(line, edge_lines):
    length = geometry.get_line_length(line)
    clean = False

    angle_thresh = 2
    dist_thresh = 5
    length_thresh = 5
    if length < length_thresh:
        clean = True
    for edge_line in edge_lines:
        diff = geometry.get_angle_diff(line, edge_line)
        dist = geometry.get_min_dist_line_segments(line, edge_line)
        if (diff < angle_thresh):
            if (dist<dist_thresh):
                clean = True
    return clean
    

def merge_lines(lines, edge_lines = [], circle=False):
    merged_lines = general_merge.merge(lines, get_merged_line, make_check_line_merge_criteria(circle))
    merged_lines = clean_merge_lines(merged_lines, edge_lines)
    return merged_lines
