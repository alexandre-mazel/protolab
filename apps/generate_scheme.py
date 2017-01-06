

import cv2
import numpy as np

import protolab.image
import protolab.geometry


im = cv2.imread("/tmp2/blank.jpg")

listWords = [
["Rest"],
["Learn"],
["Staff People", "Customer"],
]

sx = im.shape[1];

rThickness = 1.;
colorText = (0,0,0)

y=50;
dy = 100;
rMarginRect = 10;
for words in listWords:
    dx = sx/(len(words)+1)
    x = dx;
    for word in words:
        textSize = cv2.getTextSize( word, cv2.FONT_HERSHEY_SIMPLEX, rThickness, 1 );
        print( str( textSize ) );
        xt = x-(textSize[0][0]/2);
        yt = y
        cv2.putText( im, word, (xt, yt), cv2.FONT_HERSHEY_SIMPLEX, rThickness, colorText );
        cv2.rectangle(im, (xt-rMarginRect, yt+rMarginRect), (xt+textSize[0][0]+rMarginRect, yt-20-rMarginRect), colorText)
        
        x+= dx;
    y+=dy
    
cv2.imshow( "scheme", im );
cv2.waitKey(0)

