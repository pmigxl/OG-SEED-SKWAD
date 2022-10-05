# import the necessary libraries 
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy
import sys
import math
import smbus
import smbus2
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

#lcd stuff

lcd_columns = 16
lcd_rows = 2

i2c = board.I2C()
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.clear()

#address information for communication 
abus = smbus.SMBus(1)
address = 0x2a
slave_address = 20

#initlize variables 
angle = 0
data = 0

#write information to arduino/lcd and print if there are errors
def writeNumber(writeThis):
    try:
        abus.write_byte(address,writeThis)
    except:
        print('io error')
    
    try:
        data = ""
        for i in range(0,3):
            data += chr(abus.read_byte(address));
        print(data)
        print('\n')
    except:
        print('io error')
    
    tpos = ''
    if ( writeThis == 0 ):
        tpos = '00'
    elif ( writeThis == 1 ):
        tpos = '090'
    elif ( writeThis == 2 ):
        tpos = '180'
    elif ( writeThis == 3 ):
        tpos = '270'
    lcd.message = 'Curr: ' + str(data) + '\nTest: ' + str(tpos) 
    
    return -1

    

#lcd setpoint funcction
def readLCD(setpoint):
    
    setPrint = 'Setpoint: ' + str(setpoint)
    lcd.message = setPrint 




#Start continous capture 
cap = cv2.VideoCapture(0)
while(True):
  
    ret, frame = cap.read()
    #convert to grey scale and find center of the camera
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgSize = img.shape
    xSize = (imgSize[1] / 2)
    ySize = (imgSize[0] / 2)
    
    #initilize parameters and select an aruco dictionary 
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
    
    #enter loop if an id is detected 
    if len(corners)> 0:
        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4,2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            #add drawing overlay to the image 
            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
            
            # find the center of the marker 
            pX = int((topLeft[0] + bottomRight[0]) / 2.0)
            pY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
    
            # determine the quadrant 
            if pX > xSize and pY < ySize:
                angle = 1
            elif pX > xSize and pY > ySize:
                angle = 2
            elif pX < xSize and pY > ySize:
                angle = 3
            elif pX < xSize and pY < ySize:
                angle = 0
            # Display on frame
            anglePrint = str(angle) + ' degrees'
            cv2.putText(frame, anglePrint, (topRight[0], topRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
            writeNumber(angle)
          
        # show the frame 
        cv2.imshow('Image', frame)
    else:
        cv2.imshow('Image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
