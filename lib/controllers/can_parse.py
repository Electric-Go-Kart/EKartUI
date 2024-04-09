import subprocess
import os
import logging
import struct
import signal
import sys
from multiprocessing.shared_memory import SharedMemory
import atexit

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List to keep track of shared memory objects for cleanup
shared_memory_objects = []

def close_shared_memory():
    logging.info("Cleaning up shared memory...")
    for shm in shared_memory_objects:
        try:
            shm.close()
            shm.unlink()
        except Exception as e:
            logging.error(f"Error closing/unlinking shared memory: {e}")

# Register the cleanup function with atexit to ensure it runs on normal exit
atexit.register(close_shared_memory)

def signal_handler(sig, frame):
    logging.info('Terminating: You pressed Ctrl+C!')
    sys.exit(0)

# Register signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Function to create and manage shared memory
def create_shared_memory(name, size):
    try:
        shm = SharedMemory(name=name, create=True, size=size)
        shared_memory_objects.append(shm)  # Add to the list for cleanup
        logging.info(f"Created shared memory for {name}")
        return shm
    except Exception as e:
        logging.error(f"Error creating shared memory for {name}: {e}")
        raise

# Main function
def main():
    # Start subprocess
    try:
        process = subprocess.Popen(['candump', 'can0', '-L'], stdout=subprocess.PIPE, universal_newlines=True)
    except:
        logging.error("Error starting candump process. Make sure can-utils package is installed.")
        return

    # Create shared memory segments
    try:
        can_packet_status_shm = create_shared_memory("can_packet_status", 8) # B0 - B3: RPM*1, B4 - B5: Current*10, B6 - B7: Duty Cycle*1000
        can_packet_status2_shm = create_shared_memory("can_packet_status2", 8) # B0 - B3: Total Amp Hrs Consumed*10000, B4 - B7: Total Regen Amp Hrs*10000
        can_packet_status3_shm = create_shared_memory("can_packet_status3", 8) # B0 - B3: Watt Hrs Used*10000, B4 - B7: Watt Hrs Charged*10000
        can_packet_status4_shm = create_shared_memory("can_packet_status4", 8) # B0 - B1: Temp FET*10, B2 - B3: Temp Motor*10, B4 - B5: Current In*10, B6 - B7: PID Position*50
        # Below could be used in future versions
        can_packet_status5_shm = create_shared_memory("can_packet_status5", 8) # B0 - 3: Tachometer*6, B4 - 5: Voltage In*10
        can_packet_status6_shm = create_shared_memory("can_packet_status6", 8) # B0 - 1: ADC1*1000, B2 - 3: ADC2*1000, B4 - 5: ADC3*1000, B6 - 7: PPM*1000
    except Exception as e:
        logging.error("Failed to create shared memory segments. Exiting...")
        return

    # Main loop to parse CAN data
    try:
        parse_can_data(process, can_packet_status_shm, can_packet_status2_shm, can_packet_status3_shm, can_packet_status4_shm, can_packet_status5_shm, can_packet_status6_shm)
    finally:
        process.terminate()
        process.wait()

def parse_can_data(process, can_packet_status_shm, can_packet_status2_shm, can_packet_status3_shm, can_packet_status4_shm, can_packet_status5_shm, can_packet_status6_shm):
    logging.info("Entering CAN parsing loop...")
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            logging.info("Check that the can network is up")
            break
        if output:
            logging.info("Output: " + output.strip())
            
            timestamp, interface, data = output.strip().split(" ", 2)
            can_id, raw_data = data.split("#", 1)

            can_id = int(can_id, 16)
            raw_data = int(raw_data, 16)
            
            if can_id == 2305: # HEX: 0x09 (command ID) + 0x01 (VESC ID)
                rpm = raw_data >> 32 # from the most significant 32 bits (4 bytes)
                curr_all_units = (raw_data >> 16) & 0xFFFF # from the middle 16 bits (2 bytes)
                latest_duty_cycle = raw_data & 0xFFFF # from the least significant 16 bits (2 bytes)
                logging.info("RPM: " + str(rpm * 1))
                logging.info("Total current in all units: " + str(curr_all_units / 10))
                logging.info("Latest duty cycle: " + str(latest_duty_cycle / 1000))
                
                # write all the info into the can_packet_status shared memory
                can_packet_status_shm.buf[:] = struct.pack(">IHH", rpm, curr_all_units, latest_duty_cycle)


            elif can_id == 3585: # HEX: 0x0E (command ID) + 0x01 (VESC ID)
                total_amphrs_consumed = raw_data >> 32 # from the most significant 32 bits (4 bytes)
                total_regen_hrs = raw_data & 0xFFFFFFFF # from the least significant 32 bits (4 bytes)
                logging.info("Total amp hours consumed by unit: " + str(total_amphrs_consumed / 10000))
                logging.info("Total regen amp hours back into batt: " + str(total_regen_hrs / 10000))

                # write all the info into the can_packet_status2 shared memory
                can_packet_status2_shm.buf[:] = struct.pack(">II", total_amphrs_consumed, total_regen_hrs)
                
            elif can_id == 3841: # HEX: 0xOF (command ID) + 0x01 (VESC ID)
                wh_used = raw_data & 0xFFFFFFFF # from the least significant 32 bits (4 bytes)
                wh_charged = (raw_data >> 32) & 0xFFFFFFFF # from the most significant 32 bits (4 bytes)
                logging.info("Watt hours used: " + str(wh_used / 10000))
                logging.info("Watt hours charged: " + str(wh_charged / 10000))

                # write all the info into the can_packet_status3 shared memory
                can_packet_status3_shm.buf[:] = struct.pack(">II", wh_used, wh_charged)
                
            elif can_id == 4097: # HEX: 0x10 (command ID) + 0x01 (VESC ID)
                # Extracting bytes from raw_data
                temp_fet_raw = raw_data & 0xFFFF  # B0-B1 from the least significant 16 bits
                temp_motor_raw = (raw_data >> 16) & 0xFFFF  # B2-B3 from the middle 16 bits
                current_in_raw = (raw_data >> 32) & 0xFFFF  # B4-B5
                pid_pos_raw = (raw_data >> 48) & 0xFFFF  # B6-B7 from the most significant 16 bits
                # Printing unpacked values
                logging.info("Temperature FET: " + str(temp_fet_raw / 10))
                logging.info("Temperature Motor: " + str(temp_motor_raw / 10))
                logging.info("Current In: " + str(current_in_raw / 10))
                logging.info("PID Position: " + str(pid_pos_raw / 50))

                # write all the info into the can_packet_status4 shared memory
                can_packet_status4_shm.buf[:] = struct.pack(">HHHH", temp_fet_raw, temp_motor_raw, current_in_raw, pid_pos_raw)
                
            ### COMMANDS NEVER SEEN ###
            elif can_id == 6913: # HEX: 0x1B (command ID) + 0x01 (VESC ID)
                tachometer = raw_data & 0xFFFFFFFF
                voltage_in = (raw_data >> 32) & 0xFFFF
                logging.info("Tachometer: " + str(tachometer / 6))
                logging.info("Voltage In: " + str(voltage_in / 10))

                # write all the info into the can_packet_status5 shared memory
                can_packet_status5_shm.buf[:] = struct.pack(">II", tachometer, voltage_in)
                
            elif can_id == 7169: # HEX: 0x28 (command ID) + 0x01 (VESC ID)
                adc1 = raw_data & 0xFFFF 
                adc2 = (raw_data >> 16) & 0xFFFF
                adc3 = (raw_data >> 32) & 0xFFFF
                ppm = (raw_data >> 48) & 0xFFFF
                logging.info("ADC1: " + str(adc1 / 1000))
                logging.info("ADC2: " + str(adc2 / 1000))
                logging.info("ADC3: " + str(adc3 / 1000))
                logging.info("PPM: " + str(ppm / 1000))

                # write all the info into the can_packet_status6 shared memory
                can_packet_status6_shm.buf[:] = struct.pack(">HHHH", adc1, adc2, adc3, ppm)
            ### END COMMANDS NEVER SEEN ###

    logging.info("Exiting CAN parsing loop...")

if __name__ == "__main__":
    main()
