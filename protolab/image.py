__author__ = 'lgeorge & amazel'

import cv2
import math
import numpy as np

import geometry


def imageToString( im, timestamp = 0 ):
    """
    convert a numpy image to a string, so we can send it thru a remote
    return: { "timestamp": 3512123123, "width": 320, "height": 240, "channels": 1 or 3, "data": [data1, data2, ...] }
    """
    aDict = {};
    aDict["timestamp"] = timestamp;
    aDict["width"] = im.shape[1];
    aDict["height"] = im.shape[0];
    aDict["channels"] = im.shape[2];
    aData = im.reshape( im.shape[1]*im.shape[0]*im.shape[2] );
    aDict["data"] = aData.tolist();
    return aDict
    
    
def reddish(pt):
    """
    return the reddishity of a point  [-510,255]. The biggest the reddest
    """
    return int(pt[2]) - pt[1] -  pt[0];
    
    
def drawArrow( image, p, q, color, nArrowMagnitude = 9, nThickness=1, nLineType=8, nShift=0 ):
    # ported from http://mlikihazar.blogspot.fr/2013/02/draw-arrow-opencv.html
    
    #Draw the principle line
    cv2.line( image, p, q, color, nThickness, nLineType, nShift);
    
    #compute the angle alpha
    angle = math.atan2( float(p[1]-q[1]), float(p[0]-q[0]) );
    
    #compute the coordinates of the first segment
    p = ( 
                int( round( q[0] +  nArrowMagnitude * math.cos(angle + math.pi/4) ) ),
                int( round( q[1] +  nArrowMagnitude * math.sin(angle + math.pi/4) ) )
            );
                
    #Draw the first segment
    cv2.line(image, p, q, color, nThickness, nLineType, nShift);
    
    #compute the coordinates of the second segment
    p = ( 
                int( round( q[0] +  nArrowMagnitude * math.cos(angle - math.pi/4) ) ),
                int( round( q[1] +  nArrowMagnitude * math.sin(angle - math.pi/4) ) )
            );
    #Draw the second segment
    cv2.line(image, p, q, color, nThickness, nLineType, nShift);

def findCircles( img_color ):
    """
    find the circle in an image, 
    return the 4 positions [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], ] in range[0..1]
    the first will be the red one, following point will always be in the same order
    """
        
    img = cv2.cvtColor( img_color, cv2.cv.CV_BGR2GRAY );

    img = cv2.GaussianBlur( img, (3, 3), 5 );
    
    #~ img = cv2.pyrDown( img ); # PyrDown only divide by 2
    
    if( img.shape[1] == 320 ):
        p1 = 10; p2 = 20; r=5;R=10;
    else:
        p1 = 180; p2 = 35; r=8;R=60;
    

    # Apply the Hough Transform to find the circles
    circles = cv2.HoughCircles( img, cv2.cv.CV_HOUGH_GRADIENT,dp=1, minDist = img.shape[0]/16, param1=p1,param2=p2,minRadius=r,maxRadius=R );
    if( circles == None ):
        return [];
    circles = np.int16(np.around(circles))[0] # round the list and remove one level
    #~ print circles  # a list of x,y,radius    
    print( "nbr detected circles: %s" % len(circles) );
    #~ return circles;
    if( len(circles) != 4 ):
        return circles
    
    # search for the red one:
    nIdxRed = 0;
    maxRed = reddish(img_color[circles[0][1],circles[0][0]]);
    #~ print( "maxRed: %d" % maxRed );
    for idx in range( 1, len(circles) ):
        val = reddish(img_color[ circles[idx][1], circles[idx][0] ]);
        if( val > maxRed ):
            maxRed = val;
            nIdxRed=idx;
    
    ret = [];
    ret.append( [ circles[nIdxRed][0], circles[nIdxRed][1] ] );

    circles = np.delete(circles, nIdxRed,axis=0);
    
    
    # return the other one in the right order
    
    # find the farest
    nIdx = -1;
    nDistMax = 0;
    for i in range( len(circles) ):
        dist = geometry.squared_distance( ret[0], circles[i] );
        if( dist > nDistMax ):
            nDistMax = dist;
            nIdx = i;
        #print( "dist:%s" % dist );
        
    ret.append( [ circles[nIdx][0], circles[nIdx][1] ] );
    circles = np.delete(circles, nIdx,axis=0);
    
    #find the two other (ordering the dot product seems to work, cool)
    nIdx = -1;
    nDistMax = 0;    
    for i in range( len(circles) ):
        val = np.dot( geometry.vect(ret[0],ret[1]), geometry.vect(ret[0],circles[i] ) );
        #~ print( "val:%s" % val );
        if( val > nDistMax ):
            nDistMax = val;
            nIdx = i;
            
    ret.insert( 1, [ circles[nIdx][0], circles[nIdx][1] ] );
    circles = np.delete(circles, nIdx,axis=0);
    if( len(circles)>0):
        ret.append( [ circles[0][0], circles[0][1] ] );
    
    #~ ret.append( [ circles[nIdxRed][0], circles[nIdxRed][1] ] );
    return ret;
# findCircles - end

def getRotationFrom4Circles( img ):
    """
    get the rotation of the 4 circles shape.
    return an angle in radians [0..2*pi] or None if no angle detected
    """
    circles = findCircles( img );
    if( len(circles)== 4 ):    
        dir = geometry.vect(circles[0], circles[1] );
        rAngle = math.atan2( -dir[1], dir[0] );
        #~ print( "rAngle: %5.2fdeg" % (rAngle*180/math.pi) )
        return rAngle;
    return None;
# getRotationFrom4Circles - end
        
        