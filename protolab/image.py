# -*- coding: utf-8 -*-

__author__ = 'lgeorge & amazel'

import cv2
import math
import numpy as np

import geometry

class StdCamera:
    def __init__(self):
        self.cameraMatrixRef1080 = np.array([[  1.10561144e+03 ,  0.00000000e+00 ,  6.42505603e+02], [  0.00000000e+00 ,  1.11245814e+03 ,  4.96053152e+02], [  0.00000000e+00 ,  0.00000000e+00 ,  1.00000000e+00]])
        self.aCameraMatrix = []; # intrinsics for each resolution
        for rScale in [ 0.125, 0.25, 0.5, 1.0 ]:
            self.aCameraMatrix.append( self.cameraMatrixRef1080 * rScale );         # scale ratio compared to 640x480, for example in 320x240 scale ratio = 0.5, in 1280x960 scale ration = 2 , calibration matrix has been computed based on 640x480 resolution
            
        self.distorsionCoef = np.array([[ -3.14724137e-03],[  3.09723474e-01],[  1.13771499e-03],[  5.07460018e-05],[  3.39670453e+00],[  6.74398801e-03],[  7.48274002e-01],[  2.14113693e+00]])

    def getCameraMatrix( self, nWidth = 160 ):
        if( nWidth == 160 ):
            nResolution = 0;
        elif( nWidth == 320 ):
            nResolution = 1;
        elif( nWidth == 640 ):
            nResolution = 2;
        elif( nWidth == 1280 ):
            nResolution = 3;            
        else:
            assert( ("unknown resolution: %d" % nWidth) == 0 );
        assert( nResolution >= 0 and nResolution < len(self.aCameraMatrix) );
        return self.aCameraMatrix[nResolution];

    def getDistorsionCoef( self ):
        return self.distorsionCoef;
        
# class StdCamera - end

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
    
def blueish(pt):
    """
    return the reddishity of a point  [-510,255]. The biggest the reddest
    """
    return int(pt[0]) - pt[1] -  pt[2];
        
    
    
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

def findCircles( img_color, cColor = 'r', bDebug = False ):
    """
    find the circle in an image, 
    return the 4 positions [ [x1,y1], [x2,y2], [x3,y3], [x4,y4], ] in range[0..1]
    the first will be the red one, following point will always be in the same order
    - cColor: the first letter of the first color
        - 'r': red circle with 3 other black/blue one .
        - 'b': blue circle with 3 other black
    """
    if( bDebug ):
        bRender = True;
    else:
        bRender = False;
    
    img = cv2.cvtColor( img_color, cv2.cv.CV_BGR2GRAY );

    if( cColor == 'g' ):
        img = cv2.GaussianBlur( img, (3, 3), 5 );
    else:
        if( img.shape[1] <= 160 ):
            img = cv2.GaussianBlur( img, (3, 3), 5 );
        elif( img.shape[1] <= 320 ):
            img = cv2.GaussianBlur( img, (5, 5), 5 ); # TODO: tune me!
        elif( img.shape[1] <= 320 ):
            img = cv2.GaussianBlur( img, (7, 7), 5 ); # TODO: tune me!
        elif( img.shape[1] <= 1280 ):
            img = cv2.GaussianBlur( img, (15, 15), 10 );
    
    #~ img = cv2.pyrDown( img ); # PyrDown only divide by 2
    
    #~ cv2.imshow( "mat", img );
    #~ cv2.waitKey(0)
    
    if( img.shape[1] == 320 ):
        p1 = 10; p2 = 20; r=5; R=10;
    else:
        p1 = 180; p2 = 35; r=8; R=60;

    if( cColor == 'b' ):
        p1 = 80; p2 = 35; r=16; R=img.shape[1]/2;
    

    # Apply the Hough Transform to find the circles
    circles_detected = cv2.HoughCircles( img, cv2.cv.CV_HOUGH_GRADIENT,dp=1, minDist = img.shape[0]/16, param1=p1,param2=p2,minRadius=r,maxRadius=R );
    #~ print( "circles_detected: %s" % circles_detected );  # a list of x,y,radius    
    if( circles_detected == None ):
        return [];
    circles = np.int16(np.around(circles_detected))[0] # round the list and remove one level
    if( bRender ):
        # draw the outer circle
        for idx,circ in enumerate(circles):
            cv2.circle(img_color,(circ[0],circ[1]),circ[2],(0,255,255),2)    

    #~ print( "circles: %s" % circles );
    print( "nbr detected circles: %s" % len(circles) );
    #~ return circles;
    if( len(circles) != 4 ):
        if( bRender ):
            cv2.imshow( "circles", img_color );
            cv2.waitKey(0)            
        return circles;
        
    # check all radius are equal:
    rRadius = circles[0][2];
    for circle in circles[1:]:
        if(1-(rRadius/float(circle[2])) > 0.2 ):
            print( "WRN:findCircles: mismatch radius: %s !~= %s" % ( rRadius, circle[2] ) );
            return [];
    
        
    # search for the red one:
    colorFunc = reddish;
    if( cColor == 'b' ):
        colorFunc = blueish;    
    nIdxColored = 0;
    maxColored = colorFunc(img_color[circles[0][1],circles[0][0]]);
    #~ print( "maxRed: %d" % maxRed );
    for idx in range( 1, len(circles) ):
        val = colorFunc(img_color[ circles[idx][1], circles[idx][0] ]);
        if( val > maxColored ):
            maxColored = val;
            nIdxColored=idx;
    
    ret = [];
    ret.append( [ circles[nIdxColored][0], circles[nIdxColored][1] ] );

    circles = np.delete(circles, nIdxColored,axis=0);
    
    # find the two other (ordering the dot product seems to work, cool)
    # NO IT DOESN'T !    
    #~ nIdx = -1;
    #~ nValMax = 0;
    #~ for i in range( len(circles) ):
        #~ val = np.dot( geometry.vect(ret[0],ret[1]), geometry.vect(ret[0],circles[i] ) );
        #~ print( "val:%s" % val );
        #~ if( val > nValMax ):
            #~ nValMax = val;
            #~ nIdx = i;    
    
    
    # return the other one in the right order (nearest, then nearest then ...)
    for i in range(2):    
        nIdx = geometry.find_nearest( ret[-1], circles );
        #~ print( "DBG: findCircles: nearest is: %d at %d,%d" % (nIdx, circles[nIdx][0],circles[nIdx][1]) );
        ret.append( [ circles[nIdx][0], circles[nIdx][1] ] );
        circles = np.delete(circles, nIdx,axis=0);
    ret.append( [ circles[0][0], circles[0][1] ] );
        
    #~ ret.append( [ circles[nIdxColored][0], circles[nIdxColored][1] ] );
    #~ print( "DBG: findCircles: returning: %s" % str(ret) );
    
    #~ center = geometry.center( ret[0], ret[2] );
    #~ print( "a: %s" % geometry.angle( geometry.vect( center, ret[0] ), geometry.vect( center, ret[3] ) ) );
    # TODO: en fait on aimerait toujours retourner les points dans le sens des aiguilles d'une montre (par exemple), or j'arrive pas a trouver la bonne formule !!!
    
    if( bRender ):
        for idx,circ in enumerate(ret):
            # draw the outer circle
            cv2.circle(img_color,(circ[0],circ[1]),10,(0,255,255*idx),2)    
            if( idx < 2 ):
                # draw the center of the circle
                cv2.circle( img_color,(circ[0],circ[1]),2,(255,0,255),3)                
            cv2.putText( img_color, str(idx+1), (circ[0]+12,circ[1]+12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0) );
                
        cv2.imshow( "circles", img_color );
        cv2.waitKey(0)                
        
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

class WallCircleBoard:
    def __init__( self ):
        # distance between center in mm: we compute the medium between internal and external distance. w external: 549mm internal: 180 => 364.5 h: 414-46 => 230
        self.w = 364.5
        self.h = 230.0
        self.cColor = 'b'
    def size( self ):
        return (self.w,self.h);

def findCirclesPos( im, boardConfiguration, cColor = 'r', bDebug = False ):
    """
    compute the distance and orientation of the circles board
    - boardConfiguration: (w,h): the real distance in mm between each center
    return: [x,y,d,t] or None
        - x: side distance of the camera in mm (+ is to the left from the camera)
        - y: elevation distance in mm (+ is to the top from the camera)
        - d: distance between robot and circles (in mm)
        - rx: angle around the robot x angle in radians [0..2*pi]
    """
    circles = findCircles( im, cColor, bDebug = bDebug );
    print( "INF: findCirclesPos: circles: %s" % circles );
    
    if( len(circles) < 4 ):
        return None;
    #avgx = circles[0][0] - circles[0][0];
    
    #~ aCameraMatrix = camera.camera.aCameraMatrix[nResolution]
    #~ aDistorsionCoefs = camera.camera.distorsionCoef    
    a = np.array( [ +boardConfiguration[0]/2, +boardConfiguration[1]/2, 0 ] ); # the blue one
    b = np.array( [ +boardConfiguration[0]/2, -boardConfiguration[1]/2, 0 ] );
    c = np.array( [ -boardConfiguration[0]/2, -boardConfiguration[1]/2, 0 ] );
    d = np.array( [ -boardConfiguration[0]/2, +boardConfiguration[1]/2, 0 ] );

    aRealPts = np.array([a, b, c, d])
    
    for i in range( len(circles) ):
        circles[i][0] = float( circles[i][0] );
        circles[i][1] = float( circles[i][1] );
        
    aImPts = np.array( circles );
    
    cameraMatrix = StdCamera().getCameraMatrix(im.shape[1]);
    distCoeffs = StdCamera().getDistorsionCoef();
    retPnp = cv2.solvePnP( aRealPts, aImPts, cameraMatrix, distCoeffs );
    print( "DBG: findCirclesPos: retPnp: %s" % str(retPnp) );    
    bSuccess = retPnp[0];
    aRotVector = retPnp[1];
    aTransVector = retPnp[2];
    
    distX1 = circles[0][0] - circles[3][0];
    distX2 = circles[1][0] - circles[2][0];
    distX = (distX1+distX2)/2
    distY1 = circles[0][1] - circles[1][1];
    distY2 = circles[3][1] - circles[2][1];
    distY = (distY1+distY2)/2
    avg = math.sqrt(distX*distX+distY*distY);
    print( "distX1: %s, distX2: %s, avgX: %s, distY1: %s, distY2: %s, avgY: %s, avg: %s" % (distX1, distX2, distX, distY1, distY2, distY, avg) );
    
    retVal = [aTransVector[0][0],aTransVector[1][0],aTransVector[2][0]*1.09,aRotVector[2][0]];
    return retVal;
# findCirclesPos - end    

def oneShotTest_findCirclesPos():
    strFilename = "/tmp/camera_viewer_0000_0.png";
    im = cv2.imread( strFilename );
    pos = findCirclesPos(im, WallCircleBoard().size(), WallCircleBoard().cColor, bDebug = True );        
    print( "INF: autotest_findCirclesPos: pos: %s" % pos );
#~ oneShotTest_findCirclesPos();
#~ exit(0);


def autotest_findCirclesPos():
    # laser at 53cm (hors tout a 49cm d'un coté et 49.5 de l'autre):
    # QQVGA: [[130, 94], [38, 92], [38, 32], [132, 34]]            
    # QVGA: [[130, 94], [38, 92], [38, 32], [132, 34]]
    # VGA: [[130, 94], [38, 92], [38, 32], [132, 34]]                
    files = ["wall_circles_qqvga_0m59", "wall_circles_qvga_0m59", "wall_circles_vga_0m59", "wall_circles_4vga_0m59", "wall_circles_vga_2m00", "wall_circles_vga_rot_2m00", "wall_circles_vga_trans_2m00",  "wall_circles_vga_3m00" ];
    #~ files = ["wall_circles_4vga_0m59"]
    #~ files = ["wall_circles_vga_rot_2m00"]
    theoricalResults = [0,0,0];
    for file in files:
        strFilename = "../data/circles_board/wall_circles/%s.png" % file;
        print( "INF: testing on strFilename: %s" % strFilename );
        im = cv2.imread( strFilename );
        pos = findCirclesPos(im, WallCircleBoard().size(), WallCircleBoard().cColor, bDebug = True  );        
        print( "INF: autotest_findCirclesPos: pos: %s" % pos );
        if( pos != None ):
            rTheoricDistance = int(file[-4])*1000+int(file[-2:])*10;        
            rCurrentDist = pos[2];
            print( "rTheoricDistance: %f, mesured: %s" % ( rTheoricDistance, rCurrentDist ) )
            print( "ratioDistance: %f" % (rTheoricDistance/rCurrentDist) );
        else:
            assert(0);
    

if __name__ == "__main__":
    autotest_findCirclesPos();