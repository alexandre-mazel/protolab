import numpy as np

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
    