import subprocess
import os
from multiprocessing.shared_memory import SharedMemory

def close_shared_memory(shm):
    shm.close()
    shm.unlink()

# CAMs note: This is running candump and looking at can version -can0. "can0" is not referring to master or slave ESC ID
print("first")
process = subprocess.Popen(['candump', 'can0', '-L'], stdout=subprocess.PIPE, universal_newlines=True)
rpm_shm = SharedMemory(name="rpm", create=True, size=32)
rpm_buffer = rpm_shm.buf
temp_rpm = 0
rpm_buffer[:] = temp_rpm.to_bytes(32, byteorder='big')

print("second")
current_shm = SharedMemory(name="current", create=True, size=16)
current_buffer = current_shm.buf
temp_current = 0
current_buffer[:4] = temp_current.to_bytes(4, byteorder='big')

print("third")
try:
    watt_hr_shm = SharedMemory(name="watt_hr", create=False)
except FileNotFoundError:
    watt_hr_shm = SharedMemory(name="watt_hr", create=True, size=16)
watt_hr_buffer = watt_hr_shm.buf
temp_watt_hr = 0
watt_hr_buffer[:4] = temp_watt_hr.to_bytes(4, byteorder='big')

print("good")
Iterations = 10000
NUM_ITERATIONS = Iterations
KNOWN_CAN_IDS = []
CAN_UNSORTED = ""

print("Entering Loop: ")

try:
    while True:
        # while statement is blocked until there is a new line to read
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print("Output: " + output.strip() + "\n")
            
            timestamp, interface, data = output.strip().split(" ",2)
            can_id, raw_data = data.split("#",1)

            can_id = int(can_id, 16)
            raw_data = int(raw_data, 16)
            
            if can_id == 2305:
                rpm = raw_data >> 32
                curr_all_units = (raw_data >> 16) & 0xFFFF
                latest_duty_cycle = raw_data & 0xFFFF
                print("RPM: " + str(rpm))
                print("Total current in all units * 10: " + str(curr_all_units))
                print("Latest duty cycle * 1000: " + str(latest_duty_cycle))
                
                rpm_buffer[:] = rpm.to_bytes(32, byteorder='big')
                current_buffer[:] = curr_all_units.to_bytes(16, byteorder='big')
                
            elif can_id == 142:
                total_amphrs_consumed = raw_data >> 32
                total_regen_hrs = raw_data & 0xFFFFFFFF
                print("Total amp hours consumed by unit * 10000: " + str(total_amphrs_consumed))
                print("Total regen amp hours back into batt * 10000: " + str(total_regen_hrs))
                
            if NUM_ITERATIONS > 0:
                print(str(NUM_ITERATIONS))
                NUM_ITERATIONS -= 1
                
                CAN_UNSORTED += timestamp + " " + interface + " " + data + "\n"
                
                if len(KNOWN_CAN_IDS) == 0:
                    KNOWN_CAN_IDS.append({"id": can_id, "raw_data": [raw_data]})
                else:
                    for can_info in KNOWN_CAN_IDS:
                        if can_info.get("id") == can_id:
                            can_info.get("raw_data").append(raw_data)
                            break
                    else:
                        KNOWN_CAN_IDS.append({"id": can_id, "raw_data": [raw_data]})
                        
            elif NUM_ITERATIONS == 0:
                print("Finished Running Test!")
                
                CAN_INFO_FILE = open("CAN_INFO_SORTED.txt" ,"w")
                Header = """This file contains sorted data from the can bus generated from 'can_parse.py' and currently records {Iterations} CAN bus Interactions.
                The purpose of this file is to give some insight into the CAN data given from the command: candump. All CanIds and Data shown in this
                file are in Hex.
                
                Found CAN IDs:
                """
                for CanData in KNOWN_CAN_IDS:
                    Header += hex(CanData.get("id"))[2:].upper() + " "
                Header += "\n\nCANID" + "{:<8}".format("RAW DATA")
                for CanData in KNOWN_CAN_IDS:
                    Header += "\n\nid: " + hex(CanData.get("id"))[2:].upper() + "\n"
                    for RawData in CanData.get("raw_data"):
                        Header += "\t\t" + hex(RawData)[2:].upper() +"\n" 
                CAN_INFO_FILE.write(Header)
                CAN_INFO_FILE.close()
                print("Created CAN_INFO_SORTED.txt")
                
                RAW_INFO_FILE = open("CAN_INFO_RAW.txt", "w")
                RAW_INFO_FILE.write(CAN_UNSORTED)
                RAW_INFO_FILE.close()
                print("Created CAN_INFO_RAW.txt")
                
                NUM_ITERATIONS = -1
                
except KeyboardInterrupt:
    pass

finally:
    process.terminate()
    process.wait()
    close_shared_memory(rpm_shm)
    close_shared_memory(current_shm)
    close_shared_memory(watt_hr_shm)
