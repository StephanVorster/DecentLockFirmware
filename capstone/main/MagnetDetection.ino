// MagnetDetection.ino

int hallSensorPin = 2;  // Hall Effect Sensor input pin

void setupMagnetDetection() {
  pinMode(hallSensorPin, INPUT);
  Serial.begin(9600); // Optional: for debugging
}

void loopMagnetDetection() {
  int sensorValue = digitalRead(hallSensorPin);

  if (sensorValue == LOW) {
    Serial.println("Magnet detected!");
  } else {
    Serial.println("No magnet detected.");
  }

  delay(1000); // Add a delay to reduce serial output speed
}
