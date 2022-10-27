> Demo 1 Purpose: Design a system that rotates and moves a given distance/angle based on user input 


**Computer Vision:** *Alexis Capitano*
Updated_CompVisionI2C

- [x] Detect Aruco marker with camera
- [x] Calculate angle between marker and center of camera 
- [x] Provide angle output and detection status to the LCD 

To use this program, run the code on the raspberry pi with the LCD plugged in and present an aruco marker to the camera. 
Angle detection and LCD display should follow. 
**Localization:** *Preston Miglaw*

- [x] Detect position of the encoder
- [x] Identify which direction the encoder needs to move to reach new position
- [x] Spin encoder to new position

**Simulation and Control:** *Matt Lange*

- [x] Created a program that reads the encoder counts to a varible and outprints the radians and angular velocity
- [x] Designed a transfer function from the step response of angular velocity and voltage
- [x] Implemented a PI controller using the transfer function values

**System Integration:** *Brittany Ellington*

- [x] Send back current position at regular intervals
- [x] Display Setpoint and Actual Position on LCD screen by the Pi
- [x] Determine Pi Address and Slave Address

