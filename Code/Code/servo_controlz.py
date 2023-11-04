import serial
import time

# Define constants based on the LX-1501 communication protocol
LOBOT_SERVO_FRAME_HEADER = 0x55
LOBOT_SERVO_MOVE_TIME_WRITE = 1

# Function to calculate the checksum
def lobot_checksum(buf):
    temp = 0
    for b in buf:
        temp += b
    temp = ~temp & 0xFF
    return temp

# Function to send commands to move the servo
def lobot_serial_servo_move(ser, id, position, time):
    buf = bytearray()
    buf.append(LOBOT_SERVO_FRAME_HEADER)
    buf.append(LOBOT_SERVO_FRAME_HEADER)
    buf.append(id)
    buf.append(7)
    buf.append(LOBOT_SERVO_MOVE_TIME_WRITE)
    buf.append(position & 0xFF)
    buf.append((position >> 8) & 0xFF)
    buf.append(time & 0xFF)
    buf.append((time >> 8) & 0xFF)
    buf.append(lobot_checksum(buf[2:]))
    ser.write(buf)

# Main function to control the servo
def main():
    # Initialize the serial port
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    ser.flush()

    id = 1  # Set the servo ID

    while True:
        # Move the servo to different positions
        lobot_serial_servo_move(ser, id, 500, 1000)
        time.sleep(2)
        lobot_serial_servo_move(ser, id, 1000, 1000)
        time.sleep(2)

# Execute the main function
if __name__ == '__main__':
    main()
