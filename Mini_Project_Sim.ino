

#define volt_pin 9
int sampling_rate = 8;
int motor_volt = 0;
int time - 0;
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
  // put your main code here, to run repeatedly:
  
  millis(1000);
  motor_volt = analogWrite(volt_pin);
  motor_volt = motor_volt + 1;
  millis(sampling_rate);
  Serial.print();
  
}
