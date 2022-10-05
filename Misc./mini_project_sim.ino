//CPR should be CPR = 64
//Equation to convert to rad/sec: angle = C/CPR * 2pi
#include <Encoder.h>
#define motor_pin 2
int sample_rate = 1600;
float CPR = 20;
unsigned long timer = 0;
float motor_voltage;
int encodeCount;
float degree;
float rad;
float ang_vel;
int read;
Encoder myEnc(5,2);
void setup() {
  timer = 0;
  Serial.begin(19200);
}

void loop() {
  //used to measure the time in increments and display to the serial monitor
  timer = millis();
  while(millis() < timer + sample_rate){
    //analogWrite(motor_pin,0);
    //analogWrite(motor_pin,255);
    if((timer >= 1000)&&(timer <= 5000)){
      
      //prints out the encoder count values
      encodeCount = (myEnc.read())/4;
      Serial.println("encoder value: ");
      Serial.print(encodeCount);
      Serial.println("");
      //prints out the angle in degrees
      degree = (encodeCount/CPR)*360;
      Serial.println("Angle in degrees: ");
      Serial.print(degree);
      Serial.print(" degrees");
      Serial.println("");
      //prints out the angle in rads
      rad = (encodeCount/CPR)*(2*3.14159);
      Serial.print("Angle in radians: ");
      Serial.print(rad);
      Serial.print(" rads");
      Serial.println("");
      //prints out the time in milli
      Serial.println("Time: ");
      Serial.print(millis());
      Serial.print(" milli-sec");
      Serial.println("");
      //prints out the angular velocity
      ang_vel = rad/(millis()/1000);
      Serial.println("Angular velocity");
      Serial.print(ang_vel);
      Serial.print(" rads/sec");
      Serial.println("");
      read = analogRead(motor_pin);
      motor_voltage = read * (5/1023.0);
      Serial.println("Voltage");
      Serial.print(motor_voltage);
      Serial.print(" volts");
      Serial.println("");
      Serial.println("");
    }
    
  }
  
}
