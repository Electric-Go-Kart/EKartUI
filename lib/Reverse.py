
import RPi.GPIO as GPIO
import sys

# Set the pin numbering mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up pin 26 as an output pin
GPIO.setup(37, GPIO.OUT)

# Get the command from the terminal
command = sys.argv[1]

# Check the command and set the pin state accordingly
if command == "high":
    GPIO.output(37, GPIO.HIGH)
    print("Pin 26 set to HIGH")
elif command == "low":
    GPIO.output(37, GPIO.LOW)
    print("Pin 26 set to LOW")
else:
    print("Invalid command. Please use 'high' or 'low'.")

# Clean up GPIO settings
GPIO.cleanup()
