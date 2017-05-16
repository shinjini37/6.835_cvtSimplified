from scipy import optimize
import numpy as np
import math

import general_merge
import line_merge

import geometry

def get_mean(vals):
    length = len(vals)
    total = sum(vals)
    return float(total)/length

def get_merged_circle(circles):
    x = get_mean([circle[0] for circle in circles])
    y = get_mean([circle[1] for circle in circles])
    r = get_mean([circle[2] for circle in circles])
    
    return [x, y, r]

def check_circle_merge_criteria(ref_circle, test_circle):
    r = ref_circle[2]
    r_thresh = .1*r
    cent_dist_thresh = .2*r
    
    merge = False
    r_diff = abs(r - test_circle[2])
    if (r_diff < r_thresh):
        cent_dist = geometry.get_dist(ref_circle[:2], test_circle[:2])
        if (cent_dist<cent_dist_thresh):
            merge = True
    return merge

def check_line_in_list(test_line, lines):
    tx1,tx2,ty1,ty2 = test_line[0]
    idxs = []
    for i in xrange(len(lines)):
        line = lines[i]
        for x1,x2,y1,y2 in line:
            if ((x1 == tx1) and (x2 == tx2) and (y1 == ty1) and (y2 == ty2)):
                idxs.append(i)
    in_line = (len(idxs) > 0)
    return in_line, idxs

def clean_lines(match_lines_list, lines):
    lines_copy = lines[:]
    for match_lines in match_lines_list:
        for line in match_lines:
            in_lines, idxs = check_line_in_list(line, lines_copy)
            temp = []
            old_len = len(lines_copy[:])
            if in_lines:
                for i in xrange(old_len):
                    if (i not in idxs):
                        temp.append(lines_copy[i])
                lines_copy = temp
##                print old_len
##                print len(temp)
    return lines_copy

def get_match_lines(circle, lines, growing = True):
    x = circle[0]
    y = circle[1]
    r = circle[2]
    line_dist_thresh = 5#min(max(.2*r, 3), 20) #dependent on r

    match_lines = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            diff1 = abs(geometry.get_dist([x1, y1], [x,y]) - r)
            diff2 = abs(geometry.get_dist([x2, y2], [x,y]) - r)
            diff3 = abs(geometry.get_dist(geometry.get_midpoint(line), [x,y]) - r)

            length = geometry.get_dist([x1, y1], [x2, y2])
            if (diff1<line_dist_thresh and diff2<line_dist_thresh and diff3<line_dist_thresh):
                match_lines.append(line)
    return match_lines

def is_close(a,b,thresh):
    return abs(a-b)<thresh

def get_best_fit_circle(circle, lines):
    done = False
    cent_thresh = 0.025
    r_thresh = 0.025
    residu_thresh = 0.5
    ratio_thres = .8
    radius_thresh = 5
    max_iter = 500
    num_iter = 0
    while not done:
        
        x = circle[0]
        y = circle[1]
        r = circle[2]
    
        # check which lines fall close to the circumference of the circle
        match_lines = get_match_lines(circle, lines)
        
        # do circle fit on points and check that the circle is good approx of given
        points = []
        for line in match_lines:
            for x1,y1,x2,y2 in line:
                points.append([x1, y1])
                points.append([x2, y2])
                points.append(geometry.get_midpoint(line))
##        print 'points', points
        if len(points)>0:
            xc, yc, R, residu = circle_fit(points)
            got_circle = [xc, yc, R]

##            print (xc,x),(yc,y),(R,r)
            if is_close(xc, x, cent_thresh*R) and is_close(yc, y, cent_thresh*R) and is_close(R, r, r_thresh*R):
                done = True
            else:
                circle = got_circle
        else:
            return None

        num_iter += 1
        if num_iter>max_iter:
            done = True
    R = circle[2]

##    print got_circle
##    print residu 
    if (R>radius_thresh): 
        if (residu<residu_thresh):        
            arc_length = 2*math.pi*R
            line_length = 0
            for line in match_lines:
                for x1,y1,x2,y2 in line:
                    length = geometry.get_dist([x1, y1], [x2, y2])
                    line_length += length
            ratio = line_length/float(arc_length)
##            print line_length, arc_length, ratio
##            print 
            if ratio>ratio_thres:
    ##            line_length = 0
    ##            merged_lines = line_merge.merge_lines(match_lines, circle=True)
    ##            for line in merged_lines:
    ##                for x1,y1,x2,y2 in line:
    ##                    length = geometry.get_dist([x1, y1], [x2, y2])
    ##                    line_length += length
    ##
    ##            ratio = line_length/float(arc_length)
                if ratio>ratio_thres:
##                    print "taken"
    ##                print match_lines
                    return circle, match_lines, line_length, residu

    return None                
    
def get_best_circles(circles, lines):
##    print len(circles[0])
    
##    angle_thresh = math.radians(30)
    residu_thresh = 20
    best_circles = []
    got_circles = []
    match_lines_list = []
    for circle in circles[0]:
        x = circle[0]
        y = circle[1]
        r = circle[2]
        result = get_best_fit_circle(circle, lines)
##        print result
        if result is None:
            continue
        got_circle, match_lines, line_length, residu = result

        best_circles.append(circle)#(circle, got_circle, match_lines))
        got_circles.append(got_circle)
        match_lines_list.append(match_lines)
        

##    print len(got_circles)
##    print got_circles
    got_circles = general_merge.merge(got_circles, get_merged_circle, check_circle_merge_criteria)
##    print len(got_circles)
##    print got_circles
    
##    print len(best_circles)
##    print best_circles
    cleaned_lines = clean_lines(match_lines_list, lines)
    return got_circles, cleaned_lines, best_circles
            
            

def circle_fit(points):
    # from https://gist.github.com/lorenzoriano/6799568
    def calc_R(x,y, xc, yc):
        """ calculate the distance of each 2D points from the center (xc, yc) """
        return np.sqrt((x-xc)**2 + (y-yc)**2)

    def f(c, x, y):
        """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
        Ri = calc_R(x, y, *c)
        return Ri - Ri.mean()

    x = [point[0] for point in points]
    y = [point[1] for point in points]
    
    x_m = np.mean(x)
    y_m = np.mean(y)
    
    center_estimate = x_m, y_m
    center, ier = optimize.leastsq(f, center_estimate, args=(x,y))
    xc, yc = center
    Ri       = calc_R(x, y, *center)
    R        = Ri.mean()
    residu   = math.pow(np.sum((Ri - R)**2), .5)/len(Ri)

    return xc, yc, R, residu
     

##print clean_lines([[[[1, 1, 1, 1]]]], [[[1, 1, 1, 1]], [[1, 1, 2, 1]]])
##print clean_lines([[[[1, 1, 1, 1]]]], [[[1, 1, 1, 1]], [[1, 1, 1, 1]]])
##print clean_lines([[[[1, 1, 1, 1]], [[1, 1, 1, 2]]]], [[[1, 1, 1, 1]], [[1, 1, 1, 1]]])
