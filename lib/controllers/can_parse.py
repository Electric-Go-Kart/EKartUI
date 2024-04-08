import subprocess
import os
import logging
import struct
from multiprocessing.shared_memory import SharedMemory

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def close_shared_memory(shm):
    shm.close()
    shm.unlink()

try:
    process = subprocess.Popen(['candump', 'can0', '-L'], stdout=subprocess.PIPE, universal_newlines=True)
except:
    logging.error("Error starting candump process. Make sure can-utils package is installed.")

try:
    logging.info("Creating shared memory for RPM")
    rpm_shm = SharedMemory(name="rpm", create=True, size=32)
    rpm_buffer = rpm_shm.buf
    temp_rpm = 0
    rpm_buffer[:] = temp_rpm.to_bytes(32, byteorder='big')
except Exception as e:
    logging.error(f"Error creating shared memory for RPM: {e}")

try:
    logging.info("Creating shared memory for Current")
    current_shm = SharedMemory(name="current", create=True, size=16)
    current_buffer = current_shm.buf
    temp_current = 0
    current_buffer[:4] = temp_current.to_bytes(4, byteorder='big')
except Exception as e:
    logging.error(f"Error creating shared memory for Current: {e}")

try:
    logging.info("Creating shared memory for Watt-hour")
    watt_hr_shm = SharedMemory(name="watt_hr", create=True, size=16)
    watt_hr_buffer = watt_hr_shm.buf
    temp_watt_hr = 0
    watt_hr_buffer[:4] = temp_watt_hr.to_bytes(4, byteorder='big')
except Exception as e:
    logging.error(f"Error creating shared memory for Watt-hour: {e}")

try:
    logging.info("Creating shared memory for FET Temperature")
    fet_temp_shm = SharedMemory(name="fet_temp", create=True, size=8)
    fet_temp_buffer = fet_temp_shm.buf
    temp_fet_temp = 0
    fet_temp_buffer[:] = temp_fet_temp.to_bytes(8, byteorder='big')
except Exception as e:
    logging.error(f"Error creating shared memory for FET Temperature: {e}")

try:
    logging.info("Creating shared memory for Motor Temperature")
    motor_temp_shm = SharedMemory(name="motor_temp", create=True, size=8)
    motor_temp_buffer = motor_temp_shm.buf
    temp_motor_temp = 0
    motor_temp_buffer[:] = temp_motor_temp.to_bytes(8, byteorder='big')
except Exception as e:
    logging.error(f"Error creating shared memory for Motor Temperature: {e}")

try:
    logging.info("Creating shared memory for Tachometer")
    tachometer_shm = SharedMemory(name="tachometer", create=True, size=8)
    tachometer_buffer = tachometer_shm.buf
    temp_tachometer = 0
    tachometer_buffer[:] = temp_tachometer.to_bytes(8, byteorder='big')
except Exception as e:
    logging.error(f"Error creating shared memory for Tachometer: {e}")

logging.info("Entering can parsing loop")

try:
    while True:
        # while statement is blocked until there is a new line to read
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logging.info("Output: " + output.strip())
            
            timestamp, interface, data = output.strip().split(" ", 2)
            can_id, raw_data = data.split("#", 1)

            can_id = int(can_id, 16)
            raw_data = int(raw_data, 16)
            
            if can_id == 2305: # HEX: 0x09 (command ID) + 0x01 (VESC ID)
                rpm = raw_data >> 32
                curr_all_units = (raw_data >> 16) & 0xFFFF
                latest_duty_cycle = raw_data & 0xFFFF
                logging.info("RPM: " + str(rpm))
                logging.info("Total current in all units * 10: " + str(curr_all_units))
                logging.info("Latest duty cycle * 1000: " + str(latest_duty_cycle))
                
                rpm_buffer[:] = rpm.to_bytes(32, byteorder='big')
                current_buffer[:] = curr_all_units.to_bytes(16, byteorder='big')
                
            elif can_id == 3585: # HEX: 0x0E (command ID) + 0x01 (VESC ID)
                total_amphrs_consumed = raw_data >> 32
                total_regen_hrs = raw_data & 0xFFFFFFFF
                logging.info("Total amp hours consumed by unit * 10000: " + str(total_amphrs_consumed))
                logging.info("Total regen amp hours back into batt * 10000: " + str(total_regen_hrs))
                
            elif can_id == 3841: # HEX: 0xOF (command ID) + 0x01 (VESC ID)
                wh_used = raw_data & 0xFFFFFFFF
                wh_charged = (raw_data >> 32) & 0xFFFFFFFF
                logging.info("Watt hours used: " + str(wh_used))
                logging.info("Watt hours charged: " + str(wh_charged))
                
            elif can_id == 4097: # HEX: 0x10 (command ID) + 0x01 (VESC ID)
                # Extracting bytes from raw_data
                temp_fet_raw = raw_data & 0xFFFF  # B0-B1
                temp_motor_raw = (raw_data >> 16) & 0xFFFF  # B2-B3
                current_in_raw = (raw_data >> 32) & 0xFFFF  # B4-B5
                pid_pos_raw = (raw_data >> 48) & 0xFFFF  # B6-B7

                # Printing extracted bytes for debugging purposes
                logging.info("Temperature FET (Raw): " + hex(temp_fet_raw))
                logging.info("Temperature Motor (Raw): " + hex(temp_motor_raw))
                logging.info("Current In (Raw): " + hex(current_in_raw))
                logging.info("PID Position (Raw): " + hex(pid_pos_raw))

                try:
                    # Unpacking each byte and applying scale
                    temp_fet = temp_fet_raw / 10
                    temp_motor = temp_motor_raw / 10
                    current_in = current_in_raw / 10
                    pid_pos = pid_pos_raw / 50

                    # Printing unpacked values
                    logging.info("Temperature FET: " + str(temp_fet) + " °C")
                    logging.info("Temperature Motor: " + str(temp_motor) + " °C")
                    logging.info("Current In: " + str(current_in) + " A")
                    logging.info("PID Position: " + str(pid_pos) + " degrees")
                except Exception as e:
                    logging.error(f"Error unpacking raw data: {e}")
                
            ### COMMANDS NEVER SEEN ###
            elif can_id == 6913: # HEX: 0x1B (command ID) + 0x01 (VESC ID)
                tachometer = raw_data & 0xFFFFFFFF
                voltage_in = (raw_data >> 32) & 0xFFFF
                logging.info("Tachometer: " + str(tachometer))
                logging.info("Voltage In: " + str(voltage_in / 10) + " V")
                
            elif can_id == 7169: # HEX: 0x28 (command ID) + 0x01 (VESC ID)
                adc1 = raw_data & 0xFFFF
                adc2 = (raw_data >> 16) & 0xFFFF
                adc3 = (raw_data >> 32) & 0xFFFF
                ppm = (raw_data >> 48) & 0xFFFF
                logging.info("ADC1: " + str(adc1 / 1000) + " V")
                logging.info("ADC2: " + str(adc2 / 1000) + " V")
                logging.info("ADC3: " + str(adc3 / 1000) + " V")
                logging.info("PPM: " + str(ppm / 1000))
            ### END COMMANDS NEVER SEEN ###
            
except KeyboardInterrupt:
    logging.info("Exiting can parsing loop")
    process.terminate()
    process.wait()
    close_shared_memory(rpm_shm)
    close_shared_memory(current_shm)
    close_shared_memory(watt_hr_shm)
    close_shared_memory(fet_temp_shm)
    close_shared_memory(motor_temp_shm)
    close_shared_memory(tachometer_shm)

finally:
    process.terminate()
    process.wait()
    close_shared_memory(rpm_shm)
    close_shared_memory(current_shm)
    close_shared_memory(watt_hr_shm)
    close_shared_memory(fet_temp_shm)
    close_shared_memory(motor_temp_shm)
    close_shared_memory(tachometer_shm)