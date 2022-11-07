from cv2 import aruco
import cv2
import numpy as np
import math

angle = 0.0 

marker_size = 32

with open ('camera_cal1.npy', 'rb') as f:
    camera_matrix = np.load(f)
    camera_distortion = np.load(f)
    
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

cap = cv2.VideoCapture(0)

camera_width = 1280
camera_height = 960
camera_frame_rate = 20

#until q is pressed, images will continously be taken, converted to greyscale, and if an ID is detected the math preformed and displayed to calculate the angle 
while True:
    # Adding user input for distance
    # varDist = input('Enter a distance 1 - 10 feet: ")
    # varDist = int(varDist)
    # if not varDist:
    # continue
    # writeNumber(varDist)
    # print("RPI: Hi Arduino, I sent you ", varDist, " feet")
    

# Adding user input for angle of rotation
    # var = input('Enter an angle from 0 - 360 degrees: ")
    # varAngle = int(varAngle)
    # if not varAngle:
    # continue
    # writeNumber(varAngle)
    # print("RPI: Hi Arduino, I sent you ", varAngle, " feet")
    
    ret, frame = cap.read()

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgSize = grey.shape
    xCoord = (imgSize[1] / 2)
    yCoord = (imgSize[0] / 2)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(grey, aruco_dict, camera_matrix, camera_distortion)
    if len(corners)> 0:
        ids = ids.flatten()
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
        if ids is not None:
                detect = 1 
                aruco.drawDetectedMarkers(frame, corners)
                    
                for (markerCorner, markerID) in zip(corners, ids):
                    # extract marker corners and convert them to integers
                    corners = markerCorner.reshape((4,2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))
                    # compute and draw the center (x, y)-coordinates of the ArUco marker
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    cv2.circle(grey, (cX, cY), 4, (0, 0, 255), -1)
                    # Calculate the angle from camera to the object by using the provided formula
                    
                    
                    angle = round( (53.76/2) * ( (xCoord - cX) / xCoord))
                    
                    dist = (tvec[0][0][2]/100)
                    y = (tvec[0][0][0]/100)
                  
                    #dist = round(math.sqrt(math.pow(z,2) + math.pow(y,2)), 1)
                    anglePrint = str(angle) + ' degrees '
                    distPrint = str(dist) + ' feet'
                    printt = anglePrint + distPrint
                    # Use pixel manipulation to determine quadrants
                    
                    # Display the ID's and angle to video feed
                
                
                #rvec_list_all, tvec_list_all, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
                    
                #rvec= rvec_list_all[0][0]
                #tvec = tvec_list_all[0][0]
                
                #aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, tvec, 100)
                
                #rvec_flipped = rvec * -1
                #tvec_flipped = tvec * -1
                #rotation_matrix, jacobian = cv2.Rodrigues(rvec_flipped)
                #realworld_tvec = np.dot(rotation_matrix, tvec_flipped)
                
                #pitch, roll, yaw = rotationMatrixToEulerAngles(rotation_matrix)
                #angle = math.degrees(yaw)
                #tvec_str = "x=%4.0f y%4.0f angle=%4.0f"%(realworld_tvec[0], realworld_tvec[1], math.degrees(yaw))
                #cv2.putText(grey, anglePrint, (topRight[0], topRight[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
                cv2.putText(frame, printt, (20,460), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)
                #cv2.putText(frame, tvec_str, (20,460), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)
   
        
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
  
cap.release()
cv.destroyAllWindows()