#include <DualMC33926MotorShield.h>
#include <Encoder.h>

double pie = 3.14159;
bool flag;
const int motor_counts = 3200;
const double r = 3.0; //radius of the wheel in inches

double kp = 0.40;
double ki = 0.3;

Encoder encoderM1(3, 6);
Encoder encoderM2(2, 5);
DualMC33926MotorShield md;



int M1_CLK_STATE = 0;
int M1_DT_STATE = 0;
int M2_CLK_STATE = 0;
int M2_DT_STATE = 0;



double wheelThetaStart1;
double wheelThetaStart2;
double wheelDistStart1;
double wheelDistStart2;
double deg = -180;
double diameter = .9; // feet
double distance = 3.141 * diameter * deg / 360;



double enc1_double;
double enc2_double;
double enc2_OUT;

unsigned long currentTime, previousTime;
double elapsedTime;
double error;
double lastError;
double input, output, setPoint;
double totalError, rateError;


void setup() {
  Serial.begin(115200);
  md.init();
  setPoint = 0;
}


void loop() {

  long enc1 = encoderM1.read();
  double wheelTheta1 = (2.0 * pie * (double)enc1) / (double)motor_counts;
  double wheelDistance1 = (wheelTheta1 * r) / 12;


  long enc2 = encoderM2.read() * -1;
  setPoint = (double)enc1;
  input = (double)enc2;
  output = computePI(input);
  delay(100);
  double wheelTheta2 = (2.0 * pie * (double)enc2) / (double)motor_counts;
  double wheelDistance2 = (wheelTheta2 * r) / 12;

  if ((wheelDistance1 > distance) && (wheelDistance2 > distance)) {
    if (deg <= 0) {
      md.setM1Speed(100);
      md.setM2Speed(-100 + output);
      Serial.print(enc1);
      Serial.print("\t");
      Serial.print(wheelDistance1);
      Serial.print("\t");
      Serial.println(wheelDistance2);
    }
  }
  else if (wheelDistance1 < distance) {
    if (deg <= 0) {
      md.setM1Speed(0);
      md.setM2Speed(0);
    }
  }
  if (wheelDistance1 < distance) {
    if (deg > 0) {
      md.setM1Speed(-100);
      md.setM2Speed(-100 + output);
      Serial.print(enc1);
      Serial.print("\t");
      Serial.print(wheelDistance1);
      Serial.print("\t");
      Serial.println(distance);
    }
  }
  else if (wheelDistance1 > distance) {
    if (deg > 0) {
      md.setM1Speed(0);
      md.setM2Speed(0);
    }
  }
  


//  else if ((wheelDistance1 == (distance + 0.3)) || (wheelDistance1 == (distance - 0.3))) {
//    md.setM1Speed(0);
//    md.setM2Speed(0);
//  }
}


//    if(deg < 0){
//    md.setM1Speed(-100);
//    md.setM2Speed(-100 + output);
//    Serial.print(enc1);
//    Serial.print("\t");
//    Serial.print(wheelDistance1);
//    Serial.print("\t");
//    Serial.println(wheelDistance2);
//    }


//  else if((wheelDistance1 < distance)&&(wheelDistance2 < distance)){
//    md.setM1Speed(100);
//    md.setM2Speed(100 + output);
//    Serial.print(enc1);
//    Serial.print("\t");
//    Serial.print(wheelDistance1);
//    Serial.print("\t");
//    Serial.println(wheelDistance2);
//  }


double computePI(double input) {
  currentTime = millis();
  elapsedTime = (double)(currentTime - previousTime) / 1000;
  error = (-setPoint) - input;
  totalError += error * elapsedTime;
  double out = kp * error + ki * totalError;
  //  Serial.print("error:");
  //  Serial.print(error);
  //    Serial.print("\t");
  //  Serial.print(totalError);
  //    Serial.print("\t");
  //    Serial.println(out);

  lastError = error;
  previousTime = currentTime;
  return out;
}
