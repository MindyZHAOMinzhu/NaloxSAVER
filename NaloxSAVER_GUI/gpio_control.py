import time
import gpiod

LED_PIN = 17
SERVO_PIN = 18

chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(LED_PIN)
servo_line = chip.get_line(SERVO_PIN)

led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
servo_line.request(consumer="Servo", type=gpiod.LINE_REQ_DIR_OUT)

def blink_led(duration=5):
    for _ in range(duration * 2):
        led_line.set_value(1)
        time.sleep(0.5)
        led_line.set_value(0)
        time.sleep(0.5)

def set_servo_angle(angle):
    duty_cycle = int(1000000 + (angle / 180) * 1000000)
    servo_line.set_value(duty_cycle)
    time.sleep(0.5)
    servo_line.set_value(0)
