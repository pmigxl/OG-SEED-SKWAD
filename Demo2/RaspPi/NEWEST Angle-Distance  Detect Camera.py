#Faster Camera, I2C in progress

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from cv2 import aruco
import numpy as np
import sys
import math
import smbus
import smbus2
import board
import threading
import pickle
import os
import pygame


counter = 0
abus = smbus.SMBus(1)
address = 0x2a
slave_address = 0x20
time.sleep(1)
i2c = board.I2C()

data = ''

# Define the thread that will continuously pull frames from the camera
class CameraBufferCleanerThread(threading.Thread):
    def __init__(self, camera, name='camera-buffer-cleaner-thread'):
        self.camera = camera
        self.last_frame = None
        super(CameraBufferCleanerThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            ret, self.last_frame = self.camera.read()

            
            
def writeNumber(comDetect, comAngle, comDist):
    global data
    if comDetect == True:
   
        try:
            if data != '234':
                data = ''
                for i in range(0,3):
                    data += chr(abus.read_byte(address))
                print(data)
            if data == '234':
                abus.write_bus(address, comDist)
                data = ''
            else:
                abus.write_byte(address, comAngle)
        except:
            None
    else:
        print('io error')

    return -1




camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 2);
camera.set(cv2.CAP_PROP_FPS, 20);
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25);
camera.set(cv2.CAP_PROP_EXPOSURE, 30);


markerSize = 27.00 
# Start the cleaning thread
cam_cleaner = CameraBufferCleanerThread(camera)


# Takes in the calibration file from separate calibration program
with open ('camera_cal1.npy', 'rb') as f:
    cameraMatrix = np.load(f)
    distCoeffs = np.load(f)


mtx = cameraMatrix
dist = distCoeffs
flag = False



while True:
    if cam_cleaner.last_frame is not None:
        img = cv2.cvtColor(cam_cleaner.last_frame, cv2.COLOR_BGR2GRAY)
       
        imgSize = img.shape
        xCoord = (imgSize[1] / 2) +1
        yCoord = (imgSize[0] / 2) +1
        # Import the dictonary of markers, define the parameters 
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        arucoParams = cv2.aruco.DetectorParameters_create()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
        # See if
        if len(corners)> 0:
            detect = 1
            counter += 1
            ids = ids.flatten() 
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerSize, mtx, dist) 
            
            for (markerCorner, markerID) in zip(corners, ids):
                
                corners = markerCorner.reshape((4,2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
                cv2.line(img, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 2)
               
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
                
                # Calculate the angle from camera to the object by using the provided formula, 53.76 == FOV of CAMERA
                actAngle = round( (53.76/2) * ( (xCoord - cX) / xCoord))
                if actAngle < -3:
                    actAngle -= 3
                elif actAngle > 3:
                    actAngle += 3
                elif actAngle < -1 and actAngle > -3:
                    actAngle -= 1
                elif actAngle > 1 and actAngle < 3:
                    actAngle += 1
                 
                #Divide by 100 to get ft
                z = (tvec[0][0][2]/100)
                y = (tvec[0][0][0]/100) 
                     
                # Calculate the distance using z-vector of tvec and y-vector of tvec to get accurate distance
                dist = round( math.sqrt(math.pow(z,2) + math.pow(y,2)) , 1) + 0.2 #Add 0.2 to compenstate for cam position on robot
                #distFromCamToMarker = round( z , 1)
                # Display the ID's and angle
                #anglePrint = str(angle) + ' degrees'
                actPrint = str(actAngle) + ' degrees'
                distPrint = str(dist) + ' ft'
                
                printt = actPrint + distPrint
                #print(distPrint)
                #cv2.putText(img, distPrint, (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
                #cv2.putText(img, actPrint, (topRight[0], topRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (25, 255, 0), 2)
                cv2.putText(img, printt, (20,460), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)
                #writeNumber(angle)
               
        # show the output image
        cv2.imshow('Image', img)

    else:
        detect = 0 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
writeNumber(detect, actAngle, dist)
#End feed
camera.release()
cv2.destroyAllWindows()
