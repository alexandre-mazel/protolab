import math

def vect( pt1,pt2):
    return [pt2[0]-pt1[0],pt2[1]-pt1[1]]
    
def median( pt1,pt2):
    return [ (pt2[0]+pt1[0])/2, (pt2[1]+pt1[1])/2 ];
    
def add( pt, nIncrease ):
    """
    add a constant to a shape
    """
    for i in range(len(pt)):
        pt[i] += nIncrease
    return pt
    
def compute_shape_median( pts ):
    """
    compute the median of a shape (the mean)
    """
    ptsum = [0,0]
    for pt in pts:
        ptsum[0] += pt[0]
        ptsum[1] += pt[1]
    ptsum[0] /= len(pts)
    ptsum[1] /= len(pts)
    return ptsum
    
def squared_distance(pt1,pt2):
    #~ print( "DBG: squared_distance: pt1: %s" % str(pt1) );
    #~ print( "DBG: squared_distance: pt2: %s" % str(pt2) );
    return (pt2[0]-pt1[0])*(pt2[0]-pt1[0]) + (pt2[1]-pt1[1])*(pt2[1]-pt1[1]);
    
    
def computeBoudingBox( pts ):
    """
    return the bounding box [topleft, bottomright] of a list of pts (returned points could be absent from pts)
    """
    topleft = pts[0][:]
    bottomright = pts[0][:]
    for pt in pts[1:]:
        if( pt[0] < topleft[0] ):
            topleft[0] = pt[0]
        elif( pt[0] > bottomright[0] ):
            bottomright[0] = pt[0]
        if( pt[1] < topleft[1] ):
            topleft[1] = pt[1]
        elif( pt[1] > bottomright[1] ):
            bottomright[1] = pt[1]
    return [topleft, bottomright]
    

def distance(pt1,pt2):
    #~ print( "DBG: distance: pt1: %s" % str(pt1) );
    #~ print( "DBG: distance: pt2: %s" % str(pt2) );
    val = float(pt2[0]-pt1[0])*(pt2[0]-pt1[0]) + float(pt2[1]-pt1[1])*(pt2[1]-pt1[1]);
    #~ print( "DBG: distance: 1: %s" % str((pt2[0]-pt1[0])*(pt2[0]-pt1[0])) );
    #~ print( "DBG: distance: val: %s" % str(val) );
    return math.sqrt( val );
    
def center(pt1,pt2):    
    return [(pt1[0]+pt2[0])/2, (pt1[1]+pt2[1])/2];
    
def find_nearest( pt, listpts ):
    """
    find in listpts the nearest element to pt
    return the idx
    """
    nIdx = -1;
    nDistMin = 1e9;
    for i in range( len(listpts) ):
        dist = squared_distance( pt, [float(listpts[i][0]),float(listpts[i][1])] ); # convert to float and to a standard array to suppress a warning: "RuntimeWarning: overflow encountered in short_scalars"
        if( dist < nDistMin ):
            nDistMin = dist;
            nIdx = i;
    return nIdx;

    
def compute_distance_shape_to_point_return_dist_and_pt( shape, pt ):
    """
    compute the distance between a point and the nearest point in the shape
    return the distance and the point
    """
    idxNear = find_nearest( pt, shape )
    rDist = distance( shape[idxNear], pt )
    return [rDist, shape[idxNear]]

    
def compute_distance_shape_to_points( shape, pts ):
    """
    return the sum of the distance between each pt in pts and the nearest point in the shape
    """
    rDist = 0
    for pt in pts:
        idxNear = find_nearest( pt, shape )
        rDist += distance( shape[idxNear], pt )
    return rDist    
    
def compute_distance_rect_to_point_return_dist_and_pt( recttopleft, rectbottomright, pt ):
    """
    compute the distance between pt and the nearest point in the projected rectangle
    return a pair [distance, nearest point]
    x--------x
    |         |    
    |         |  d
    |         |-----x pt (here the distance is about 5 chars :) )
    |         |
    x--------x
    
    NB: pt could be in the rectangle
    """
    # first find the nearest segment

    # compute 4 centers
    c1 = [ (recttopleft[0]+rectbottomright[0]) / 2, recttopleft[1] ]
    c2 = [ rectbottomright[0], (recttopleft[1]+rectbottomright[1]) / 2 ]
    c3 = [ (recttopleft[0]+rectbottomright[0]) / 2, rectbottomright[1] ]
    c4 = [ recttopleft[0], (recttopleft[1]+rectbottomright[1]) / 2 ]
    idxseg = find_nearest( pt, [c1,c2,c3,c4] )
    print( "idxseg: %s" % idxseg )
    if idxseg == 0:
        pt1 = recttopleft
        pt2 = [ rectbottomright[0], recttopleft[1] ]
        # computing point (should be easier than that, but...)
        neary = recttopleft[1]
        nearx = pt[0]
        if nearx < recttopleft[0]:
            nearx = recttopleft[0]
        elif nearx > rectbottomright[0]:
            nearx = rectbottomright[0]
    elif idxseg == 1:
        pt1 = [ rectbottomright[0], recttopleft[1] ]
        pt2 = rectbottomright
        nearx = rectbottomright[0]
        neary = pt[1]
        if neary < recttopleft[1]:
            neary = recttopleft[1]
        elif neary > rectbottomright[1]:
            neary = rectbottomright[1]        
    elif idxseg == 2:
        pt1 = rectbottomright
        pt2 = [ recttopleft[0], rectbottomright[1] ]
        neary = rectbottomright[1]
        nearx = pt[0]
        if nearx < recttopleft[0]:
            nearx = recttopleft[0]
        elif nearx > rectbottomright[0]:
            nearx = rectbottomright[0]        
    else:
        pt1 = [ recttopleft[0], rectbottomright[1] ]
        pt2 = recttopleft
        nearx = recttopleft[0]
        neary = pt[1]
        if neary < recttopleft[1]:
            neary = recttopleft[1]
        elif neary > rectbottomright[1]:
            neary = rectbottomright[1]        

        
    #~ pt1:pt2 = nearest seg
    
    # with a,b,c length of every segment (a: pt1:pt, b:pt1:pt2, c: pt2:pt)
    # s = (a+b+c)/2 # half perimeter
    # Aire = sqrt(s(s-a)(s-b)(s-c)) # formule de heron
    # Aire = (1/2)*bh
    # h = A/(0.5*b)
    a = distance(pt1,pt)
    b = distance(pt1,pt2)
    c = distance(pt2,pt)
    s = (a+b+c)/2.
    aire = math.sqrt((s*(s-a)*(s-b)*(s-c)))
    h = aire/(b*0.5)
    return ( h, (neary,neary) )
# compute_distance_rect_to_point_returnpoint - end    
    
def compute_distance_rect_to_point( recttopleft, rectbottomright, pt ):
    res = compute_distance_rect_to_point_return_dist_and_point( recttopleft, rectbottomright, pt )
    return res[0]
# compute_distance_rect_to_point - end
    
    


def angle( v1, v2 ):
    """
    return the angle between v1 and v2 (in radians)
    """
    
    return math.acos( (float(v1[0]) * v2[0] + float(v1[1]) * v2[1]) / ( math.sqrt( float(v1[0])*v1[0] + float(v1[1])*v1[1]) * math.sqrt(float(v2[0])*v2[0] + float(v2[1])*v2[1]) ) )        
    # TODO: use atan2() !!!
    
def translate_shape( pts, dir ):
    for pt in pts:
        pt[0] += dir[0]
        pt[1] += dir[1]

        
        
def autotest():
    import test
    test.assert_check_float( distance( [316, 258], [1064, 270,191] ) , 748.096 )
    test.assert_check_float( compute_distance_rect_to_point( [1,1], [8, 3], [12, 2] ), 4 )
    test.assert_check_float( compute_distance_rect_to_point( [1,1], [8, 3], [5, 10] ), 7 )
    test.assert_check_float( compute_distance_rect_to_point( [1,1], [8, 3], [1, 1] ), 0 ) # on corner
    test.assert_check_float( compute_distance_rect_to_point( [1,1], [8, 3], [2, 2] ), 1 ) # into square
    test.assert_check_float( compute_distance_rect_to_point( [1,1], [8, 3], [100, 1] ), 92 ) # on line but far


if( __name__ == "__main__" ):
    autotest();