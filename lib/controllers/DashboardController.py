import threading
import subprocess
import logging
from PySide6.QtCore import QObject, Property, Slot, Signal, QTimer
from PySide6.QtQml import QmlElement, QmlSingleton
from .CANController import CANController

QML_IMPORT_NAME = "org.ekart.DashboardController"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
@QmlSingleton
class DashboardController(QObject):
    rpmChanged = Signal(int)
    battPercentChanged = Signal(float)
    directionChanged = Signal(str)
    stateChanged = Signal(bool)
    currentChanged = Signal(float)

    def __init__(self, parent=None):
        super(DashboardController, self).__init__(parent)
        self.can_controller = CANController()
        self.can_controller.start()
        self.can_controller.rpmChanged.connect(self.updateRPM)
        self.can_controller.currentChanged.connect(self.updateCurrent)
        self.can_controller.battPercentChanged.connect(self.updateBatteryPercent)
        # variables
        self.isHeadlightOn = False
        self.dashState = "locked"
        self.direction = "parked"
        self.rpmVal = 0  
        self.currentVal = 0.0  
        self.batteryPercentage = 0.0 
        # constants
        self.num_pole_pairs = 6
        self.reverse_pin = 26
        self.wheel_circumference = 0.0001962  # in miles
        self.total_wh_cap = 144  # 12 v * 12 Ah

    # def _setup_timer(self):
    #     self.timer = QTimer(self)
    #     self.timer.timeout.connect(self._update_properties)
    #     self.timer.start(25)  # Update every _ ms

    # def _update_properties(self):
    #     self.rpmChanged.emit(self.rpmVal)
    #     self.currentChanged.emit(self.currentVal)
    #     self.battPercentChanged.emit(self.batteryPercentage)

    @Slot()
    def toggleHeadlight(self):
        self.isHeadlightOn = not self.isHeadlightOn
        print("Headlights ON!" if self.isHeadlightOn else "Headlights OFF!")

    ##############################
    # Information Property Slots #
    ##############################
    @Slot(result=str)
    def getSpeed(self):
        # multiply motor rpm by gear ratio
        # wheelrpm = (self.rpmVal*9)/30
        speed = round((self.rpmVal * self.wheel_circumference) * 60)
        if speed > 200:  # clamp it down to 0 because of CAN bus noise
            speed = 0
        return str(speed)

    @Slot(int)
    def updateRPM(self, rpm):
        if rpm > 10000:  # clamp it down to 0 because of CAN bus noise
            rpm = 0
        self.rpmVal = rpm  # Assuming rpmVal is the internal state variable for RPM
        self.rpmChanged.emit(rpm)

    @Slot(result=str)
    def getRPM(self):
        return str(self.rpmVal)

    @Slot(float)
    def updateBatteryPercent(self, percent):
        self.batteryPercentage = percent
        self.battPercentChanged.emit(percent)

    @Slot(result=str)
    def getBatteryPercent(self):
        return f'{self.batteryPercentage:.2f}'

    @Slot(float)
    def updateCurrent(self, current):
        self.currentVal = current
        self.currentChanged.emit(current)

    @Slot(result=str)
    def getCurrentVal(self):
        return str(self.currentVal)

    ############################
    # Direction Property Slots #
    ############################
    @Slot(str)
    def setDirection(self, direction):
        if (self.rpmVal == 0 and not (self.getLocked())):
            self.direction = direction
            self.directionChanged.emit(self.direction)
            print(">>>>>>>" + direction)

    @Slot(result=bool)
    def getResting(self):
        if (self.rpmVal < 50):
            return True
        else:
            return False

    @Slot(result=bool)
    def getForward(self):
        if (self.direction == "forward"):
            return True
        else:
            return False

    @Slot(result=bool)
    def getReverse(self):
        if (self.direction == "reverse"):
            return True
        else:
            return False

    @Slot(result=bool)
    def getParked(self):
        if (self.direction == "parked"):
            return True
        else:
            return False

    ########################
    # State Property Slots #
    ########################
    @Slot(str)
    def setState(self, state):
        self.dashState = state
        self.stateChanged.emit(self.dashState)
        print(">>>>>>>" + state)

    @Slot(result=str)
    def getState(self):
        return self.dashState

    @Slot(result=bool)
    def getDefault(self):
        return self.dashState == "default"

    @Slot(result=bool)
    def getLocked(self):
        return self.dashState == "locked"

    # Information Properties
    speed = Property(str, getSpeed, notify=rpmChanged)
    rpm = Property(str, getRPM, notify=rpmChanged)
    batteryPercent = Property(str, getBatteryPercent, notify=battPercentChanged)
    current = Property(str, getCurrentVal, notify=currentChanged)

    # Direction Properties
    atRest = Property(bool, getResting, notify=rpmChanged)
    forward = Property(bool, getForward, notify=directionChanged)
    reverse = Property(bool, getReverse, notify=directionChanged)
    parked = Property(bool, getParked, notify=directionChanged)

    # State Properties
    state = Property(str, getState, setState, notify=stateChanged)
    default = Property(bool, getDefault, notify=stateChanged)
    locked = Property(bool, getLocked, notify=stateChanged)

    # Add other getters and setters as needed