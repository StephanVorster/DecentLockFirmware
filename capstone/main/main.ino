void setup() {
  // Your existing setup code goes here

  // Call setup functions for magnet detection, buzzer control, PIR sensor, and button
  setupMagnetDetection();
  setupBuzzerControl();
  setupPIRSensor();
  setupButton();
}

void loop() {
  // Your existing loop code goes here

  // Call loop functions for magnet detection, buzzer control, PIR sensor, and button
  loopMagnetDetection();
  loopBuzzerControl();
  loopPIRSensor();
  loopButton();
}
