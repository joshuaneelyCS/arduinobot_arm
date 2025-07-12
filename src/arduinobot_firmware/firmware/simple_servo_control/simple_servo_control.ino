#include <Servo.h>

Servo base;

void setup() {
  
  base.attach(8 );
  base.write(0);

  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() {
  if (Serial.available()) {
    int angle = Serial.readString().toInt();
    base.write(angle);
  }

  delay(0.1);
  // elbow and gripper stay fixed in this example
}
