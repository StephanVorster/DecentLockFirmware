// BuzzerControl.ino

int buzzerPin = 8;      // Buzzer control pin

void setupBuzzerControl() {
  pinMode(buzzerPin, OUTPUT);
}

void loopBuzzerControl() {
  tone(buzzerPin, 2048);  // Generate a 2.048 kHz tone
  delay(1000);            // Duration of the tone
  noTone(buzzerPin);      // Stop the tone
  delay(1000);            // Wait for 1 second
}
