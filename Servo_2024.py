import gpiod
import time

# Define GPIO chip and pin
SERVO_PIN = 18
chip = gpiod.Chip('gpiochip4')
servo_line = chip.get_line(SERVO_PIN)

# Request the line for output
servo_line.request(consumer="SERVO", type=gpiod.LINE_REQ_DIR_OUT)

# Function to move servo to a specific angle
def set_servo_angle(angle):
    pulse_width = int((angle / 180.0) * 2000000 + 500000)  # Convert angle to nanoseconds
    servo_line.set_value(1)
    time.sleep(pulse_width / 1000000000.0)
    servo_line.set_value(0)
    time.sleep(0.02)  # Allow servo to move

try:
    print("Moving servo to 0°")
    set_servo_angle(0)
    time.sleep(2)
    
    print("Moving servo to 90°")
    set_servo_angle(90)
    time.sleep(2)
    
    print("Moving servo to 180°")
    set_servo_angle(180)
    time.sleep(2)

finally:
    servo_line.release()
    print("Servo test complete")
