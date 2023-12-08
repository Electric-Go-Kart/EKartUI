from PySide6.QtCore import QObject, Property, Slot, Signal
from PySide6.QtQml import QmlElement, QmlSingleton
from multiprocessing.shared_memory import SharedMemory
import RPi.GPIO as GPIO
import os
        
class GPIOController(QObject):
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)

    @Slot()
    def setHigh(self):
        GPIO.output(26, GPIO.HIGH)

    @Slot()
    def setLow(self):
        GPIO.output(26, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()


