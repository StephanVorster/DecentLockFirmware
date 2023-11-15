// Button.ino

const int buttonPin = 2;
int buttonState = 0;

void setupButton() {
  pinMode(buttonPin, INPUT);
  Serial.begin(9600); // Initialize serial communication
}

void loopButton() {
  buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH) {
    Serial.println("Button is pressed");
    // Add your code here for what to do when the button is pressed
  } else {
    Serial.println("Button is not pressed");
    // Add your code here for what to do when the button is not pressed
  }
  delay(100); // Add a small delay to avoid rapid serial prints
}
