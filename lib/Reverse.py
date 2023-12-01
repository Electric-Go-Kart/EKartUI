from pynput import keyboard
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

command = 'low'
def on_press(key):
    global command
    if key == keyboard.Key.up:
        command = 'high'
    elif key == keyboard.Key.down:
        command = 'low'

listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    while True:
        if command == 'high':
            GPIO.output(26, GPIO.HIGH)
        else:
            GPIO.output(26, GPIO.LOW)
        time.sleep(1)
finally:
    GPIO.cleanup()
