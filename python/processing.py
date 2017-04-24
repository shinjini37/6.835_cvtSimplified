from scipy import optimize
import numpy as np
import math

def get_best_circles(circles, lines):
    print len(circles[0])
    threshold_1 = 20
    threshold_2 = 50
    angle_thresh = math.radians(10)
    best_circles = []
    for circle in circles[0]:
        x = circle[0]
        y = circle[1]
        r = circle[2]
        # check which lines fall close to the circumference of the circle
        match_lines = []
        line_length = 0
        for line in lines:
            for x1,y1,x2,y2 in line:
                diff1 = abs(math.pow(math.pow((x1-x), 2) + math.pow((y1-y), 2), .5) - r)
                diff2 = abs(math.pow(math.pow((x2-x), 2) + math.pow((y2-y), 2), .5) - r)

                length = math.pow(math.pow((x1-x2), 2) + math.pow((y1-y2), 2), .5)
                
                if (diff1<threshold_1 and diff2<threshold_1):
                    if (length< angle_thresh*r):
                        match_lines.append(line)
                        line_length += length
        print match_lines
        # do circle fit on points and check that the circle is good approx of given
        points = []
        for line in match_lines:
            for x1,y1,x2,y2 in line:
                points.append([x1, y1])
                points.append([x2, y2])

        arc_length = 2*math.pi*r
        ratio = line_length/float(arc_length)
        if ratio>.2 and ratio <2.2:
            xc, yc, R, residu = circle_fit(points)
            got_circle = [xc, yc, R]
            diff_x = abs(xc-x)
            diff_y = abs(yc-y)
            diff_r = abs(R-r)

##            print diff_x, diff_y, diff_r, residu
##            if (diff_x<threshold_2 and diff_y<threshold_2 and diff_r<threshold_2):
##                print (line_length/float(arc_length))
##                print match_lines
            best_circles.append((circle, got_circle, match_lines))

    print len(best_circles)
##    print best_circles
    return best_circles
            
            

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
    residu   = np.sum((Ri - R)**2)

    return xc, yc, R, residu
     
    
