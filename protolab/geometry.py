
def vect( pt1,pt2):
    return [pt2[0]-pt1[0],pt2[1]-pt1[1]]
    
def median( pt1,pt2):
    return ( (pt2[0]+pt1[0])/2, (pt2[1]+pt1[1])/2);
    
def squared_distance(pt1,pt2):
    #~ print( "DBG: squared_distance: pt1: %s" % str(pt1) );
    #~ print( "DBG: squared_distance: pt2: %s" % str(pt2) );
    return (pt2[0]-pt1[0])*(pt2[0]-pt1[0]) + (pt2[1]-pt1[1])*(pt2[1]-pt1[1]);    
