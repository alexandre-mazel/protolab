
def vect( pt1,pt2):
    return [pt2[0]-pt1[0],pt2[1]-pt1[1]]
    
def median( pt1,pt2):
    return ( (pt2[0]+pt1[0])/2, (pt2[1]+pt1[1])/2);
    
def squared_distance(pt1,pt2):
    return (pt2[0]-pt1[0])*(pt2[0]-pt1[0]) + (pt2[1]-pt1[1])*(pt2[1]-pt1[1]);    
