import subprocess
from multiprocessing.shared_memory import SharedMemory
import logging

logging.basicConfig(filename='can_parse.log', level=logging.DEBUG, filemode='w')

try:
	# Edit to vcan0 or can0
	process = subprocess.Popen(['candump', 'vcan0', '-L'], stdout=subprocess.PIPE, universal_newlines=True)
	# process = subprocess.Popen(['candump', 'can0', '-L'], stdout=subprocess.PIPE, universal_newlines=True)
	# Check to see if shared memory is already created

	# Create shared memory
	rpm_shm = SharedMemory(name="rpm", create=True, size=32)
	rpm_buffer = rpm_shm.buf
	temp_rpm = 0
	rpm_buffer[:] = temp_rpm.to_bytes(32, byteorder='big')
	logging.debug("Created rpm_shm")

	current_shm = SharedMemory(name="current", create=True, size=16)
	current_buffer = current_shm.buf
	temp_current = 0
	current_buffer[:4] = temp_current.to_bytes(4, byteorder='big')
	logging.debug("Created current_shm")

	watt_hr_shm = SharedMemory(name="watt_hr", create=True, size=16)
	watt_hr_buffer = watt_hr_shm.buf
	temp_watt_hr = 0
	watt_hr_buffer[:4] = temp_watt_hr.to_bytes(4,byteorder='big')
	logging.debug("Created watt_hr_shm")

	Iterations = 10000
	NUM_ITERATIONS = Iterations
	KNOWN_CAN_IDS = []
	CAN_UNSORTED = ""

	logging.debug("Shared Memory Created... entering while loop")

	while True:
		# while statement is blocked until there is a new line to read
		output = process.stdout.readline()
		logging.debug("Output: " + output)
		
		timestamp, interface, data = output = output.strip().split(" ",2)
		can_id, raw_data = data.split("#", 1)
		
		# print("Timestamp: " + timestamp)
		# print("Interface: " + interface)
		# print("CAN ID: " + can_id)
		# print("Raw Data: " + raw_data)
		print("Output: " + timestamp + " " + interface + " " + data + "\n")

		if can_id:
			can_id = int(can_id, 16)
		else:
			logging.error("No can_id found")

		if raw_data:
			raw_data = int(raw_data, 16)
		else:
			logging.error("No raw data found")

		# can_id 2368 might not be RPM with current ESCs. Currently under investigations
		if can_id == 2305:
			rpm = raw_data >> 32
			curr_all_units = (raw_data >> 16) & 0xFFFF
			latest_duty_cycle = raw_data & 0xFFFF
			print("RPM: " + str(rpm))
			print("Total current in all units * 10: " + str(curr_all_units))
			print("Latest duty cycle * 1000: " + str(latest_duty_cycle))
			
			rpm_buffer[:] = rpm.to_bytes(32, byteorder='big')
			current_buffer[:] = curr_all_units.to_bytes(16, byteorder='big')
			
		# can_id 142 might not be total amphrs on current ESCs. Currently under Investigation	
		elif can_id == 142:
			total_amphrs_consumed = raw_data >> 32
			total_regen_hrs = raw_data & 0xFFFFFFFF
			print("Total amp hours consumed by unit * 10000: " + str(total_amphrs_consumed))
			print("Total regen amp hours back into batt * 10000: " + str(total_regen_hrs))
		
		#elif can_id == 3841:
		#	watt_hr = raw_data >> 32
		#	watt_hr_buffer[:] = watt_hrs.to_bytes(32, byteorder="big")
		
		# For CAN_SORTED_DATA no dupicate items are added. Each time code is run it check the new incomming data
		# FIXME INCOMPLETE!!!
		if NUM_ITERATIONS > 0:
			print(str(NUM_ITERATIONS))
			NUM_ITERATIONS = NUM_ITERATIONS - 1
			
			# Gather Unsorted Data
			CAN_UNSORTED += timestamp + " " + interface + " " + data + "\n"
			
			# Sort Data
			if len(KNOWN_CAN_IDS) == 0:
				KNOWN_CAN_IDS.append({"id": can_id, "raw_data": [raw_data]})
			else:
				for can_info in KNOWN_CAN_IDS:
					if can_info.get("id") == can_id:
						can_info.get("raw_data").append(raw_data)
						break
				# else statement only executes if the break statement was not reached
				else:
					KNOWN_CAN_IDS.append({"id": can_id, "raw_data": [raw_data]})

				
		# At the end of a test save the results		
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

			# So this doesnt repeat...
			NUM_ITERATIONS = -1

		return_code = process.poll()
		if return_code is not None:
			print("Return code: ", return_code)
			for output in process.stdout.readlines():
				print(output.strip())
			break
finally:
	rpm_shm.close()
	rpm_shm.unlink()
	current_shm.close()
	current_shm.unlink()
	watt_hr_shm.close()
	watt_hr_shm.unlink()
	logging.debug("Shared Memory Closed")
	process.terminate()
	process.wait()
	logging.debug("Process Terminated")
	print("Process Terminated")