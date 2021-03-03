from imutils.video import VideoStream
import imutils
import numpy as np
from numpy import asarray # import array 
import cv2
from PIL import Image
import pyfirmata
cap = cv2.VideoCapture(0)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
w, h = 480,640
"""
try:
   hardware = pyfirmata.ArduinoMega("/dev/ttyUSB0")
   led1 = hardware.get_pin('d:2:p')
   
except:

   print("Rerouting the serial communication")
   try:
        hardware = pyfirmata.ArduinoMega("/dev/ttyUSB1")
        led1 = hardware.get_pin('d:2:p')
   except:
       print("Loose connection with hardware")
"""
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    #cv2.imshow('frame',frame)
    data = asarray(frame) # Convert frame into the array for modify grid mesh height map algorithm
    print(data)
    print(data.shape)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #cv2.imshow('hsv',hsv)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    #cv2.imshow('Mask green',mask)
    heightmap = asarray(mask)
    imageout = Image.fromarray(mask)
    imageout.save('Groundheighgen.png')
    #imageout.show()

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # only proceed if the radius meets a minimum size
                if radius > 10:
                        # draw the circle and centroid on the frame
                        cv2.circle(frame, (int(x), int(y)), int(radius),
                                (0, 255, 255), 2)
                        Detector = cv2.circle(frame, center, 5, (0, 0, 255), -1)
                        #led1.write(1)
                        print("Found Green")
                        #cv2.imshow('Detector',Detector)    
                        #heightmap = asarray(Detector)
                        #imageout = Image.fromarray(Detector, 'RGB')
                        #imageout.save('Groundheighgen.png')
                        #imageout.show()
                #else:
                #    led1.write(0) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

