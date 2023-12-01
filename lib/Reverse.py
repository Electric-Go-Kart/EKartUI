import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Set up pin 26 as an output pin
GPIO.setup(26, GPIO.OUT)

# Get the command from the terminal
command = sys.argv[1]

# Check the command and set the pin state accordingly
if command == "high":
    GPIO.output(26, GPIO.HIGH)
    print("Pin 26 set to HIGH")
    time.sleep(1)  # wait for 1 second
    GPIO.output(26, GPIO.LOW)  # reset the pin
elif command == "low":
    GPIO.output(26, GPIO.LOW)
    print("Pin 26 set to LOW")
    time.sleep(1)  # wait for 1 second
    GPIO.output(26, GPIO.HIGH)  # reset the pin
else:
    print("Invalid command. Please use 'high' or 'low'.")

# Clean up GPIO settings
GPIO.cleanup()
