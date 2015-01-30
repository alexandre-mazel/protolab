# -*- coding: utf-8 -*-
"""
extract the board circle from some images as seens in data/circles_board
"""

###########################################################
#
# entete a mettre a jour
#
# Author: L. George & A. Mazel
#
# (c) 2015 Protolab
###########################################################


import cv2
import math
import numpy as np
import os
import time

def red(pt):
    """
    return the reddishity of a point  [-510,255]. The biggest the reddest
    """
    return int(pt[2]) - pt[1] -  pt[0];
    
def medt( pt1,pt2):
    return ( (pt2[0]+pt1[0])/2, (pt2[1]+pt1[1])/2);
    
def squared_distance(pt1,pt2):
    return (pt2[0]-pt1[0])*(pt2[0]-pt1[0]) + (pt2[1]-pt1[1])*(pt2[1]-pt1[1]);
    
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
    def vect( pt1,pt2):
        return [pt2[0]-pt1[0],pt2[1]-pt1[1]]
        
    img = cv2.cvtColor( img_color, cv2.cv.CV_BGR2GRAY );

    img = cv2.GaussianBlur( img, (3, 3), 5 );
    
    #~ img = cv2.pyrDown( img ); # PyrDown only divide by 2

        

    # Apply the Hough Transform to find the circles
    circles = cv2.HoughCircles( img, cv2.cv.CV_HOUGH_GRADIENT,dp=1,minDist = img.shape[0]/16, param1=180,param2=35,minRadius=8,maxRadius=60 );
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
    maxRed = red(img_color[circles[0][1],circles[0][0]]);
    #~ print( "maxRed: %d" % maxRed );
    for idx in range( 1, len(circles) ):
        val = red(img_color[ circles[idx][1], circles[idx][0] ]);
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
        dist = squared_distance( ret[0], circles[i] );
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
        val = np.dot( vect(ret[0],ret[1]), vect(ret[0],circles[i] ) );
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
    

    
#filename = "2015_01_30-14h11m26s925179ms.jpg"
strPath = "/home/likewise-open/ALDEBARAN/amazel/dev/git/protolab/data/circles_board/seq/";
listFiles = sorted(os.listdir( strPath ))
nCpt = 0;
nCptGood = 0;
timeBegin = time.time();
bRender = 1;
for filename in listFiles:
    print( "%d: filename: %s" % (nCpt,filename) );
    filename =  strPath + filename;
    if( os.path.isdir(filename) ):
        continue;
        
    img = cv2.imread( filename );
    #~ continue;
    circles = findCircles( img );
    if( bRender ):
        # render stuffs
        if( 1 ):
            # render circle
            print circles;
            for idx,circ in enumerate(circles):
                # draw the outer circle
                cv2.circle(img,(circ[0],circ[1]),10,(0,255,255*idx),2)    
                if( idx < 2 ):
                    # draw the center of the circle
                    cv2.circle(img,(circ[0],circ[1]),2,(255,0,255),3)
                
        if( len(circles)== 4 ):
            pt1 = medt(circles[0],circles[3])
            pt2 = medt(circles[1],circles[2])
            #~ cv2.line(img,pt1,pt2,(255,0,255),3);
            #~ cv2.circle(img,pt2,2,(255,0,255),5)
            drawArrow( img,pt1,pt2,(0,255,0),20, 3);
            
            nCptGood += 1;


    if(bRender):
        cv2.imshow( "mat", img );
        cv2.waitKey(1)
        
    nCpt += 1;

print( "nCptGood: %d/%d (%5.0f%%)" % (nCptGood,nCpt,nCptGood*100/float(nCpt)) ) # current: 263/281
print( "time total: %5.2fs" % (time.time() - timeBegin) ); # ~3.90s; just opening file takes 2secs
cv2.destroyAllWindows()
