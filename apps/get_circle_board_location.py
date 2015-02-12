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

import protolab.image

import cv2
import math
import numpy as np
import os
import time


def autotest():
    #filename = "2015_01_30-14h11m26s925179ms.jpg"
    strPath = "/home/likewise-open/ALDEBARAN/amazel/dev/git/protolab/data/circles_board/seq2/";
    listFiles = sorted(os.listdir( strPath ))
    nCpt = 0;
    nCptGood = 0;
    timeBegin = time.time();
    bRender = 0;
    for filename in listFiles:
        print( "%d: filename: %s" % (nCpt,filename) );
        filename =  strPath + filename;
        if( os.path.isdir(filename) ):
            continue;
            
        img = cv2.imread( filename );
        #~ continue;
        circles = protolab.image.findCircles( img );
        if( len(circles)== 4 ):    
            nCptGood += 1;
            dir = vect(circles[0], circles[1] );
            rAngle = math.atan2( -dir[1], dir[0] );
            print( "rAngle: %5.2fdeg" % (rAngle*180/math.pi) )
            
        if( bRender ):
            # render stuffs
            if( 1 ):
                # render circle
                #~ print circles;
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

        if(bRender):
            cv2.imshow( "mat", img );
            cv2.waitKey(1)
            #~ exit()
            
        nCpt += 1;

    print( "nCptGood: %d/%d (%5.0f%%)" % (nCptGood,nCpt,nCptGood*100/float(nCpt)) ) # current: 263/281 for seq1 and 12/13 for seq2
    print( "time total: %5.2fs" % (time.time() - timeBegin) ); # ~3.90s; just opening file takes 2secs
    cv2.destroyAllWindows()

# autotest - end

autotest()