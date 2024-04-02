import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
ENA = 18
IN1 = 23
IN2 = 24
ENB = 25
IN3 = 5
IN4 = 6

# Ultrasonic sensor GPIO pins
TRIG = 20
ECHO = 21

# Setup GPIO pins
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
# Ultrasonic sensor setup
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Set ENA and ENB to HIGH to enable motor driver outputs
GPIO.output(ENA, GPIO.HIGH)
GPIO.output(ENB, GPIO.HIGH)

# Define motor control functions
def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Ultrasonic sensor function
def get_distance():
    # Trigger ultrasonic sensor
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    # Wait for echo response
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 34300 cm/s
    distance = round(distance, 2)
    return distance

try:
    while True:
        distance = get_distance()
        print("Distance:", distance, "cm")

        if distance < 30:  # Adjust this threshold according to your needs
            print("Obstacle detected! Stopping the vehicle.")
            stop()
            time.sleep(1)  # Stop for 1 second
 else:
            forward()

except KeyboardInterrupt:
    stop()  # Stop motors on keyboard interrupt
    GPIO.cleanup()  # Clean up GPIO on exit
