# Title: Aruco Quadrant Dection with I2C
# Authors: Alexis Capitano, Preston Miglaw, Britanny Ellington, and Matt Lange 
# Team: 10 
# Date: 10/5/2022
# Purpose: Detect an Arcuo marker and determine which quadrant of the camera it is in. Communicate this output to an arduino and display on an LCD.
# To Use: Run this program and put an aruco marker in the field of view of the camera. The corresponding quadrant output will be displayed on the terminal and LCD and the arduino will control the motor accordingly 


# Import necessary tools 
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

# LCD and I2C info 
lcd_columns = 16
lcd_rows = 2
i2c = board.I2C()
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.clear()
abus = smbus.SMBus(1)
address = 0x2a
slave_address = 20

# Declare variables 
output = 0
info = 0

# Function to write info to the arduino and LCD, returns error if there is a communication error 
def writeNumber(variableName):
    try:
        abus.write_byte(address,variableName)
    except:
        print('io error')
    
    try:
        info = ""
        for i in range(0,3):
            info += chr(abus.read_byte(address));
        print(info)
        print('\n')
    except:
        print('io error')
    
    target = ''
    if ( variableName == 0 ):
        target = '00'
    elif ( variableName == 1 ):
        target = '090'
    elif ( variableName == 2 ):
        target = '180'
    elif ( variableName == 3 ):
        target = '270'
    lcd.message = 'Current: ' + str(info) + '\nTarget: ' + str(target) 
    
    return -1

    

# Update setpoint on LCD
def readLCD(setpoint):
    
    setpointPrint = 'Setpoint: ' + str(setpoint)
    lcd.message = setpointPrint 


# Begin Video 
cap = cv2.VideoCapture(0)

while(True):
    
    ret, frame = cap.read()
    
    # Convert frame to greyscale 
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    # Initlize the parameters and import appropriate arcuo dictionary 
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(grey, arucoDict, parameters=arucoParams)
    
    # Enter this if an ID is detected in the frame 
    if len(corners)> 0:
        
        ids = ids.flatten()
       
        for (markerCorner, markerID) in zip(corners, ids):
            
            corners = markerCorner.reshape((4,2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            
            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
            
            # Find the center of the aruco marker 
            x = int((topLeft[0] + bottomRight[0]) / 2.0)
            y = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
        
            # Find the center of the frame
            imgSize = grey.shape
            xSize = (imgSize[1] / 2)
            ySize = (imgSize[0] / 2)
            
            # Determine which quandrant the aruco marker is located in
            if x > xSize and y < ySize:
                output = 1
            elif x > xSize and y > ySize:
                output = 2
            elif x < xSize and y > ySize:
                output = 3
            elif x < xSize and y < ySize:
                output = 0
                
            # Display the information
            outputPrint = str(output) + ' degrees'
         
            cv2.putText(frame, outputPrint, (topRight[0], topRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
            writeNumber(output)
           
        cv2.imshow('Image', frame)
    else:
        cv2.imshow('Image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
