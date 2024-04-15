import subprocess
import logging
from PySide6.QtCore import QThread, Signal

class CANController(QThread):
    currentChanged = Signal(float)
    rpmChanged = Signal(int)
    battPercentChanged = Signal(float)

    def __init__(self, parent=None):
        super(CANController, self).__init__(parent)
        # constants
        self.num_pole_pairs = 6
        self.reverse_pin = 26
        self.wheel_circumference = 0.0001962  # in miles
        self.total_wh_cap = 144  # 12 v * 12 Ah
        self.max_voltage_of_battery = 14 # not needed in the future if we actually impliment a BMS
        # variables
        self.rpmVal = 0
        self.currentVal = 0.0
        self.cumulativeAh = 0
        self.cumulativeWh = 0
        self.batteryPercentage = 0

    def run(self):
        try:
            process = subprocess.Popen(['candump', 'can0', '-L'], stdout=subprocess.PIPE, universal_newlines=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self._process_output(output.strip())
        except Exception as e:
            logging.error(f"CAN parsing thread encountered an error: {e}")
        finally:
            process.terminate()
            process.wait()

    def _process_output(self, output):
        # Example processing logic; replace with your actual CAN message parsing
        timestamp, interface, data = output.split(" ", 2)
        can_id, raw_data = data.split("#", 1)

        # Mock processing, update the actual logic to process CAN data
        can_id = int(can_id, 16)
        raw_data = int(raw_data, 16)

        if can_id == 2305:  # HEX: 0x09 (command ID) + 0x01 (VESC ID)
            self.rpmVal = (raw_data >> 32) / self.num_pole_pairs  # from the most significant 32 bits (4 bytes)
            self.currentVal = ((raw_data >> 16) & 0xFFFF) / 10  # from the middle 16 bits (2 bytes)
            latest_duty_cycle = (raw_data & 0xFFFF) / 1000  # from the least significant 16 bits (2 bytes)
            logging.info("RPM: " + str(self.rpmVal))
            logging.info("Current: " + str(self.currentVal))
            logging.info("Latest duty cycle: " + str(latest_duty_cycle))

            # Emit signals to update the QML properties
            self.rpmChanged.emit(self.rpmVal)
            self.currentChanged.emit(self.currentVal)
            

        elif can_id == 3585:  # HEX: 0x0E (command ID) + 0x01 (VESC ID)
            total_amphrs_consumed = (raw_data >> 32) / 10000  # from the most significant 32 bits (4 bytes)
            total_regen_hrs = (raw_data & 0xFFFFFFFF) / 10000  # from the least significant 32 bits (4 bytes)
            logging.info("Total amp hours consumed by unit: " + str(total_amphrs_consumed))
            logging.info("Total regen amp hours consumed by unit: " + str(total_regen_hrs))
            self.cumulativeAh = total_amphrs_consumed - total_regen_hrs

        elif can_id == 3841:  # HEX: 0xOF (command ID) + 0x01 (VESC ID)
            wh_used = (raw_data & 0xFFFFFFFF) / 10000  # from the least significant 32 bits (4 bytes)
            wh_charged = ((raw_data >> 32) & 0xFFFFFFFF) / 10000  # from the most significant 32 bits (4 bytes)
            logging.info("Watt hours used: " + str(wh_used))
            logging.info("Watt hours charged: " + str(wh_charged))
            self.cumulativeWh = wh_charged - wh_used
            # Dynamically calculate voltage
            if self.cumulativeAh == 0:
                voltage = 0
                self.batteryPercentage = 0
            else:
                voltage = self.cumulativeWh / self.cumulativeAh
                self.batteryPercentage = (voltage / self.max_voltage_of_battery) * 100
            # Dynamically calculate battery percentage
            # Emit signal to update the QML property    
            if voltage > self.max_voltage_of_battery:
                # throw an error and exception
                logging.error("Battery voltage exceeds the maximum voltage of the battery at " + str(voltage) + "V")
                # TODO: Implement a BMS to prevent this from happening
                return
            self.battPercentChanged.emit(self.batteryPercentage)

        elif can_id == 4097:  # HEX: 0x10 (command ID) + 0x01 (VESC ID)
            # Extracting bytes from raw_data
            temp_fet_raw = (raw_data & 0xFFFF) / 10  # B0-B1 from the least significant 16 bits
            temp_motor_raw = ((raw_data >> 16) & 0xFFFF) / 10  # B2-B3 from the middle 16 bits
            current_in_raw = ((raw_data >> 32) & 0xFFFF) / 10  # B4-B5
            pid_pos_raw = ((raw_data >> 48) & 0xFFFF) / 50  # B6-B7 from the most significant 16 bits
            # Printing unpacked values
            logging.info("Temperature FET: " + str(temp_fet_raw))
            logging.info("Temperature Motor: " + str(temp_motor_raw))
            logging.info("Current In: " + str(current_in_raw))
            logging.info("PID Position: " + str(pid_pos_raw))

        ###########################
        ### COMMANDS NEVER SEEN ###
        ###########################
        elif can_id == 6913:  # HEX: 0x1B (command ID) + 0x01 (VESC ID)
            tachometer = (raw_data & 0xFFFFFFFF) / 6
            voltage_in = ((raw_data >> 32) & 0xFFFF) / 10
            logging.info("Tachometer: " + str(tachometer))
            logging.info("Voltage In: " + str(voltage_in))

        elif can_id == 7169:  # HEX: 0x28 (command ID) + 0x01 (VESC ID)
            adc1 = (raw_data & 0xFFFF) / 1000
            adc2 = ((raw_data >> 16) & 0xFFFF) / 1000
            adc3 = ((raw_data >> 32) & 0xFFFF) / 1000
            ppm = ((raw_data >> 48) & 0xFFFF) / 1000
            logging.info("ADC1: " + str(adc1))
            logging.info("ADC2: " + str(adc2))
            logging.info("ADC3: " + str(adc3))
            logging.info("PPM: " + str(ppm))