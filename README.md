# DecentLockFirmware
 ![simple_logo-transparent](https://github.com/StephanVorster/DecentLockFirmware/assets/48912531/872207c7-3a67-4c3d-a0f6-2aa5a0a379d9)


The Smart Lock Project aims to create a high-security smart lock system using cutting-edge technology and robust security measures. Leveraging the XRPL (Ripple Ledger) blockchain, along with biometric authentication and cloud integration, this project sets out to redefine the standards for smart lock security.

## Features

- **XRPL Integration:** Utilizes XRPL blockchain technology for secure user authentication and access control.
- **Biometric Authentication:** Incorporates fingerprint recognition for enhanced user verification.
- **Cloud Integration:** Stores lock access logs and camera footage securely on AWS S3 for easy access via the mobile app.
- **Offline Operation:** Ensures lock operation remains functional even in offline scenarios, with an Arduino Nano board controlling the lock mechanism independently from the main Raspberry Pi unit.

## Project Structure

The project consists of two main components:

1. **Mobile App:** Developed using Kotlin/Java, the mobile app provides users with a seamless interface for managing lock access, viewing camera footage, and accessing logs.
2. **Lock Firmware & QtApp:** This component includes the firmware for the smart lock hardware, implemented using C/C++ for Arduino Nano, and a Qt-based desktop application for lock configuration and management.

## Installation

1. Clone the repository to your local machine.
2. Install the necessary dependencies for both the mobile app and lock firmware.
3. Build and deploy the mobile app to your Android device.
4. Flash the lock firmware onto the Arduino Nano board.

## Usage

1. Launch the mobile app.
2. Use the app to configure lock settings.
3. Tap phone to lock to upload settings to lock
4. Test the lock's operation by tapping your phone to the lock even when your phone is locked.

## Contributing

Contributions to the Smart Lock Project are welcome! Feel free to fork the repository, make your changes, and submit a pull request.
