//CPR should be CPR = 64
//Equation to convert to rad/sec: angle = C/CPR * 2pi
//Set the CLK to pin 2 and the DT pin to pin 3, GND --> GND
#include <Encoder.h>
int sample_rate = 1600;
float CPR = 20;
unsigned long timer = 0;
int encodeCount;
float degree;
float rad;
float ang_vel;
Encoder myEnc(2, 3);
void setup() {
  timer = 0;
  Serial.begin(19200);
}

void loop() {
  //used to measure the time in increments and display to the serial monitor
  timer = millis();
  while(millis() < timer + sample_rate){
    if((timer >= 1000)&&(timer <= 5000)){
      encodeCount = (myEnc.read())/4;
      
      Serial.println("encoder value: ");
      Serial.print(encodeCount);
      Serial.println("");
      degree = (encodeCount/CPR)*360;
      Serial.println("Angle in degrees: ");
      Serial.print(degree);
      Serial.println("");
      rad = (encodeCount/CPR)*(2*3.14159);
      Serial.print("Angle in radians: ");
      Serial.print(rad);
      Serial.println("");
      Serial.println("Time: ");
      Serial.print(millis());
      Serial.print(" milli-sec");
      Serial.println("");
      ang_vel = rad/(millis()/1000);
      Serial.println("Angular velocity");
      Serial.print(ang_vel);
      Serial.println("");
      Serial.println("");
    }
    
  }
  
}
