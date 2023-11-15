// PIRSensor.ino

int pirPin = 3;         // PIR sensor output pin

void setupPIRSensor() {
  pinMode(pirPin, INPUT);
  Serial.begin(9600); // Optional: for debugging
}

void loopPIRSensor() {
  if (isMotionDetected()) {
    Serial.println("Motion detected!");
    // Add your code here for what to do when motion is detected
  } else {
    Serial.println("No motion detected.");
    // Add your code here for what to do when there's no motion
  }
}

bool isMotionDetected() {
  return digitalRead(pirPin) == HIGH;
}
