#define volt_pin 9
int sampling_rate = 8;
int motor_volt = 0;
int time = 0;
unsigned long timer = 0;


void setup() {
  //set pins 4,7,8,9, and 10 to output
  pinMode(4,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  //set the baud rate
  Serial.begin(250000);
}

void loop() {
  //Set Time1 to be millis elapsed
  timer = millis();
  while(millis() < (timer + sampling_rate)){
    //delay for 1 sec and set to desired positive value
    delay(1000);
    motor_volt = analogWrite(volt_pin);
    motor_volt = motor_volt + 1;
  }
  //print out the current time, motor voltage command, and angular velocity
  if((timer >= 1000)&&(timer <= 2000)){
  Serial.print(Time1);
  Serial.print(motor_volt);
  }
  
}
