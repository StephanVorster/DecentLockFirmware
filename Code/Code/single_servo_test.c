#include <stdint.h>
#include <wiringPi.h>
#include <wiringSerial.h>

// Macro Definitions
#define GET_LOW_BYTE(A) (uint8_t)((A))
#define GET_HIGH_BYTE(A) (uint8_t)((A) >> 8)
#define BYTE_TO_HW(A, B) ((((uint16_t)(A)) << 8) | (uint8_t)(B))
#define LOBOT_SERVO_FRAME_HEADER         0x55
#define LOBOT_SERVO_MOVE_TIME_WRITE      1

// Function to calculate checksum
uint8_t LobotCheckSum(uint8_t buf[], uint8_t len) {
    uint16_t temp = 0;
    for (uint8_t i = 2; i < len + 2; i++) {
        temp += buf[i];
    }
    temp = ~temp;
    return (uint8_t)temp;
}

// Function to move servo
void LobotSerialServoMove(int serialPort, uint8_t id, int16_t position, uint16_t time) {
    uint8_t buf[10];
    if (position < 0)
        position = 0;
    if (position > 1000)
        position = 1000;
    buf[0] = buf[1] = LOBOT_SERVO_FRAME_HEADER;
    buf[2] = id;
    buf[3] = 7;
    buf[4] = LOBOT_SERVO_MOVE_TIME_WRITE;
    buf[5] = GET_LOW_BYTE(position);
    buf[6] = GET_HIGH_BYTE(position);
    buf[7] = GET_LOW_BYTE(time);
    buf[8] = GET_HIGH_BYTE(time);
    buf[9] = LobotCheckSum(buf, 7);
    for (int i = 0; i < 10; i++) {
        serialPutchar(serialPort, buf[i]);
    }
}

int main(void) {
    // Initialize wiringPi with the Broadcom (BCM) pin numbering scheme
    wiringPiSetupGpio();
    int serialPort = serialOpen("/dev/ttyS0", 115200);
    if (serialPort < 0) {
        return 1;  // Exit if failed to open serial port
    }

    delay(1000);  // Initial delay

    #define ID1 1

    while (1) {
        // Move the servo to various positions with delays in between
        LobotSerialServoMove(serialPort, ID1, 100, 500);
        delay(1000);
        LobotSerialServoMove(serialPort, ID1, 500, 500);
        delay(1000);
        LobotSerialServoMove(serialPort, ID1, 900, 500);
        delay(1000);
        LobotSerialServoMove(serialPort, ID1, 500, 500);
        delay(1000);
    }

    // Close serial port (although this line will never be reached)
    serialClose(serialPort);

    return 0;
}
