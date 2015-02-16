# -*- coding: utf-8 -*-
# !/usr/bin/env python

""".



"""

import numpy as np
import webcam

__author__ = 'lgeorge'
__copyright__ = "Copyright 2015, Aldebaran Robotics - ProtoLab"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = 'lgeorge'
__email__ = "lgeorge@aldebaran-robotics.com"
__status__ = "Dev"


def test_getImage():
    print( 'start' )

    video_devices = webcam.get_video_devices()
    for video_device in video_devices:
        webcam_obj = webcam.WebCam(strDeviceName = video_device)
        webcam_obj.getImage()


