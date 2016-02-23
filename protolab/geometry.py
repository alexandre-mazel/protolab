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
    
def find_nearest( pt, v ):
    """
    find in v the nearest element to pt
    return the idx
    """
    nIdx = -1;
    nDistMin = 1e9;
    for i in range( len(v) ):
        dist = squared_distance( pt, [float(v[i][0]),float(v[i][1])] ); # convert to float and to a standard array to suppress a warning: "RuntimeWarning: overflow encountered in short_scalars"
        if( dist < nDistMin ):
            nDistMin = dist;
            nIdx = i;
    return nIdx;
    
def compute_distance_shape_to_points( shape, pts ):
    """
    return the sum of the distance between each pt in pts and the nearest point in the shape
    """
    rDist = 0
    for pt in pts:
        idxNear = find_nearest( pt, shape )
        rDist += distance( shape[idxNear], pt )
    return rDist
    
def compute_distance_rect_to_point( recttopleft, rectbottomright, pt ):
    return 421 # todo!


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


def _checkFloat( val, value ):
    print( "%s\n" % val );
    if( abs(val-value) > 0.01 ):
        print( "_check failed: %s != %s" % (val,value) );
        assert( 0 );
        
        
def autotest():
    val = distance( [316, 258], [1064, 270,191] );
    _checkFloat(val,748.096);


if( __name__ == "__main__" ):
    autotest();