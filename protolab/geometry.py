import math

def vect( pt1,pt2):
    return [pt2[0]-pt1[0],pt2[1]-pt1[1]]
    
def median( pt1,pt2):
    return ( (pt2[0]+pt1[0])/2, (pt2[1]+pt1[1])/2);
    
def squared_distance(pt1,pt2):
    #~ print( "DBG: squared_distance: pt1: %s" % str(pt1) );
    #~ print( "DBG: squared_distance: pt2: %s" % str(pt2) );
    return (pt2[0]-pt1[0])*(pt2[0]-pt1[0]) + (pt2[1]-pt1[1])*(pt2[1]-pt1[1]);    

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
    

def angle( v1, v2 ):
    """
    return the angle between v1 and v2 (in radians)
    """
    
    return math.acos( (float(v1[0]) * v2[0] + float(v1[1]) * v2[1]) / ( math.sqrt( float(v1[0])*v1[0] + float(v1[1])*v1[1]) * math.sqrt(float(v2[0])*v2[0] + float(v2[1])*v2[1]) ) )        
    # TODO: use atan2() !!!


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