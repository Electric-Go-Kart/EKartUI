from PySide6.QtCore import QObject, Property, Slot, Signal, QTimer
from PySide6.QtQml import QmlElement, QmlSingleton
from multiprocessing.shared_memory import SharedMemory
import math
import struct

QML_IMPORT_NAME = "org.ekart.DashboardController"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
@QmlSingleton
class DashboardController(QObject):

    # These are the signals that will be emitted to QML and are considered important data for the dashboard
    rpm_changed = Signal(int) # for calculating speed to display
    current_changed = Signal(float) # for info panel
    battery_percentage_changed = Signal(float) # for info panel
    batt_temp_changed = Signal(float) # for info panel
    motor_temp_changed = Signal(float) # for info panel
    estimated_range_changed = Signal(int) # for range display (CONCEPT)
    direction_changed = Signal(str) # for direction 
    state_changed = Signal(str) # for state

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_shared_memory()
        self.pole_pairs = 6
        self.direction = "parked"
        self.dashState = "locked"
        self.isHeadlightOn = False
        self.wheel_diameter = 0.622 # inches prob idk need a wheel
        self.gear_ratio = 1 # for direct drive e days display
        self.total_watt_hr_capacity = 144 # 12 v * 12 Ah
        self.currentVal = 0 # Calculate by dividing the raw data (B4-B5) in can_packet_status by 10
        self.rpmVal = 0 # Calculate by dividing the raw data (B0-B3) in can_packet_status by the number of pole pairs
        self.batteryPercentage = 0 # % given watt hours used and charged in can_packet_status3
        self.battTemp = 0 # Calculate by dividing the raw data (B0-B1) in can_packet_status4 by 10
        self.motorTemp = 0 # Calculate by dividing the raw data (B2-B3) in can_packet_status4 by 10
        self.estimatedRange = 0 # CONCEPT
        self.avg_watt_per_mile = 0 # CONCEPT
        QTimer.singleShot(25, self.update)  # Setup a timer to periodically call update every 25ms


    def _init_shared_memory(self):
        self.shared_memory_segments = {
            "can_packet_status" : {"name": "can_packet_status", "buffer": None, "value": 0},
            "can_packet_status2" : {"name": "can_packet_status2", "buffer": None, "value": 0},
            "can_packet_status3" : {"name": "can_packet_status3", "buffer": None, "value": 0},
            "can_packet_status4" : {"name": "can_packet_status4", "buffer": None, "value": 0},
            "can_packet_status5" : {"name": "can_packet_status5", "buffer": None, "value": 0},
            "can_packet_status6" : {"name": "can_packet_status6", "buffer": None, "value": 0}
        }

        for key, segment in self.shared_memory_segments.items():
            try:
                shm = SharedMemory(name=segment["name"])
                segment["buffer"] = shm.buf
            except FileNotFoundError:
                print(f"ERROR: Unable to connect to {segment['name']} shared memory. Check that can_parse.py is running.")
                segment["value"] = "ERROR"

    def update(self):
        # Update shared memory values and unpack correctly
        for key, segment in self.shared_memory_segments.items():
            if segment["buffer"] is not None:
                print(f"Updating {key}...")
                if key == "can_packet_status":
                    # Assuming can_packet_status was packed with '>IHH' format
                    buffer_bytes = bytes(segment["buffer"])
                    self.rpmVal, current_raw, duty_cycle_raw = struct.unpack(">IHH", buffer_bytes)
                    self.currentVal = current_raw / 10.0  # Apply scaling if needed
                    # Update the RPM value based on the number of pole pairs
                    self.rpmVal = self.rpmVal / self.pole_pairs
                    
                # elif key == "can_packet_status3":
                #     # Assuming can_packet_status3 was packed with '>II' format
                #     wh_used, wh_charged = struct.unpack(">II", segment["buffer"])
                #     remaining_wh = self.wattHrCap - wh_used + wh_charged
                #     self.batteryPercentage = (remaining_wh / self.wattHrCap) * 100
                #     self.estimatedRange = remaining_wh / avg_watt_per_mile

                # elif key == "can_packet_status4":
                #     # Assuming can_packet_status4 was packed with '>HHHH' format
                #     fet_temp_raw, motor_temp_raw, _, _ = struct.unpack(">HHHH", segment["buffer"])
                #     self.battTemp = fet_temp_raw / 10.0
                #     self.motorTemp = motor_temp_raw / 10.0

        self._emit_signals()


    def _emit_signals(self):
        self.rpm_changed.emit(self.rpmVal)
        self.current_changed.emit(self.currentVal)
        self.battery_percentage_changed.emit(self.batteryPercentage)
        self.batt_temp_changed.emit(self.battTemp)
        self.motor_temp_changed.emit(self.motorTemp)
        self.estimated_range_changed.emit(self.estimatedRange)

    

    # Speed calculation simplified for demonstration purposes
    @Slot(result=str)
    def getSpeed(self):
        wheel_circumference = self.wheel_diameter * math.pi
        speed = (self.rpmVal * wheel_circumference * 60) / (self.gear_ratio * 5280)
        return f"{speed:.2f}"

    # @Slot(result=str)
    # def getRPM(self):
    #     return str(self.shared_memory_segments["erpm"]["value"])

    # @Slot(result=float)
    # def getBatteryPercent(self):
    #     return self.batteryPercentage

    # @Slot(result=str)
    # def getCurrentVal(self):
    #     return str(self.shared_memory_segments["current"]["value"])

    # @Slot(result=int)
    # def getWatt_hrVal(self):
    #     return self.shared_memory_segments["watt_hr"]["value"]

    # @Slot(str)
    # def setDirection(self, direction):
    #     if self.shared_memory_segments["erpm"]["value"] == 0 and not self.getLocked():
    #         self.direction = direction
    #         self.directionChanged.emit(direction)
    #         print(f">>>>>>>{direction}")

    # @Slot(result=bool)
    # def getResting(self):
    #     return self.shared_memory_segments["erpm"]["value"] < 50

    # @Slot(result=bool)
    # def getForward(self):
    #     return self.direction == "forward"

    # @Slot(result=bool)
    # def getReverse(self):
    #     return self.direction == "reverse"

    # @Slot(result=bool)
    # def getParked(self):
    #     return self.direction == "parked"

    # @Slot(str)
    # def setState(self, state):
    #     self.dashState = state
    #     self.stateChanged.emit(state)
    #     print(f">>>>>>>{state}")

    # @Slot(result=str)
    # def getState(self):
    #     return self.dashState

    # @Slot(result=bool)
    # def getDefault(self):
    #     return self.dashState == "default"

    # @Slot(result=bool)
    # def getLocked(self):
    #     return self.dashState == "locked"

    # # These slots are for demonstration purposes only and don't acta
    # @Slot()
    # def toggleHeadlight(self):
    #     self.isHeadlightOn = not self.isHeadlightOn
    #     status = "ON" if self.isHeadlightOn else "OFF"
    #     print(f">>>>>>>Headlights {status}!")

    # Property definitions...
    speed = Property(str, getSpeed, notify=rpm_changed)
