import cv2
import numpy as np
import select
import time
import v4l2capture  # can be found here : https://github.com/gebart/python-v4l2capture/blob/master/capture_picture.py

def list_video_device():
    import os
    import v4l2capture
    file_names = [x for x in os.listdir("/dev") if x.startswith("video")]
    file_names.sort()
    for file_name in file_names:
        path = "/dev/" + file_name
        print path
        try:
            video = v4l2capture.Video_device(path)
            driver, card, bus_info, capabilities = video.get_info()
            print "    driver:       %s\n    card:         %s" \
                "\n    bus info:     %s\n    capabilities: %s" % (
                    driver, card, bus_info, ", ".join(capabilities))
            video.close()
        except IOError, e:
            print "    " + str(e)

class WebCam():
    """
    Access webcam(s) using video4linux (v4l2)
    eg:
        webcam = WebCam();
        im = webcam.getImage();
        cv2.imwrite( "/tmp/test.jpg", im )
    """
    def __init__( self, strDeviceName = "/dev/video0", nWidth = 640, nHeight = 480 ):
        print( "INF: WebCam: opening: '%s'" % strDeviceName );
        self.video = v4l2capture.Video_device(strDeviceName)
        # Suggest an image size to the device. The device may choose and
        # return another size if it doesn't support the suggested one.
        size_x, size_y = self.video.set_format(nWidth, nHeight)
        print( "format is: %dx%d" % (size_x, size_y) );
        # Create a buffer to store image data in. This must be done before
        # calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
        # raises IOError.
        self.video.create_buffers(30)
        # Send the buffer to the device. Some devices require this to be done
        # before calling 'start'.
        self.video.queue_all_buffers()
        # Start the device. This lights the LED if it's a camera that has one.
        self.video.start()
        print( "INF: WebCam: opening: '%s' - done" % strDeviceName );
        
    def __del__( self ):
        self.video.close()
    
    def getImage(self):
        print("INF: WebCam.getImage: Reading image...")
        # Wait for the device to fill the buffer.
        rStartAcquistion = time.time()
        aRet = select.select((self.video,), (), ()) # Wait for the device to fill the buffer.
        print( "DBG: WebCam.getImage: select return: %s" % str(aRet) );
        image_data = self.video.read_and_queue()
        rEndAquisition = time.time()
        rImageAquisitionDuration =  rEndAquisition - rStartAcquistion

        #image = Image.fromstring("RGB", (size_x, size_y), image_data)
        #image.save(strFilename)
        
        nparr = np.fromstring(image_data, np.uint8).reshape( 480,640,3)
        nparr = cv2.cvtColor(nparr, cv2.cv.CV_BGR2RGB);
        return nparr
# class WebCam - end
