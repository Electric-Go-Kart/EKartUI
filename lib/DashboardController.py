from PySide6.QtCore import QObject, Property, Slot, Signal
from PySide6.QtQml import QmlElement, QmlSingleton
from multiprocessing.shared_memory import SharedMemory

QML_IMPORT_NAME = "org.ekart.DashboardController"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
@QmlSingleton
class DashboardController(QObject):
	testPlus = True #temp var used for test code
	erpmVal = 0
	rpmVal = 0
	currentVal = 0.0
	wattHrsVal = 0.0
	wattHrsChargedVal = 0.0
	vinVal= 0.0

	# Pole pairs of motor - determined by counting number of poles inside motor
	pole_pairs = 6
	batteryPercentage = 0.0
	direction = "parked"
	dashState = "locked"
	isHeadlightOn = False
	# Set up shared memory with can_parse.py for getting ERPM data
	# Getting information from the CANBUS
	try:
		erpm_shm = SharedMemory(name="rpm")
		erpm_buffer = erpm_shm.buf
	except:
		print("ERROR: Unable to connect to can_parse RPM shared memory. Check that can_parse.py is running.")
		rpmVal = "ERROR"
	try:
		current_shm = SharedMemory(name="current")
		current_buffer = current_shm.buf
	except:
		print("ERROR: Unable to connect to can_parse CURRENT shared memory. Check that can_parse.py is running.")
		currentVal = "ERROR"
	try:
		watt_hrs_shm = SharedMemory(name="watt_hr")
		watt_hrs_buffer = watt_hrs_shm.buf
	except:
		print("ERROR: Unable to connect to can_parse WATT_HRS shared memory. Check that can_parse.py is running.")
		wattHrsVal = "ERROR"
	try:
		watt_hrs_charged_shm = SharedMemory(name="watt_hrs_charged")
		watt_hrs_charged_buffer = watt_hrs_charged_shm.buf
	except:
		print("ERROR: Unable to connect to can_parse WATT_HRS_CHARGED shared memory. Check that can_parse.py is running.")
		wattHrsChargedVal = "ERROR"
	try:
		v_in_shm = SharedMemory(name="v_in")
		v_in_buffer = v_in_shm.buf
	except:
		print("ERROR: Unable to connect to can_parse V_IN shared memory. Check that can_parse.py is running.")
		vinVal = "ERROR"

	rpmChanged = Signal(int)
	# TEST signals, to update Current, watt/hrs, watt/hrs consummed, v_in
	currentChanged = Signal(float)				# Want to display current as a float so we can see 2.5A instead of 2A or 3A.
	wattHrsChanged = Signal(float)			# Watt hrs and watt hrs charges is definalty a float
	wattHrsChargedChanged = Signal(float)
	vinChanged = Signal(float)				# Definatly want V_in to be a float so we can calc battery percentage (Impliment later)
	battPercentChanged = Signal(float)
	directionChanged = Signal(str)
	stateChanged = Signal(bool)

#Update Tick Functions
	def __init__(self, parent=None):
		QObject.__init__(self, parent)
		self.startTimer(25)		

	def timerEvent(self, event):
		self.update()


	def update(self):		
		#tempory test code
		# if self.testPlus:
			# self.batteryPercentage += 0.005
		# else:
			# self.batteryPercentage -= 0.005

		# if self.batteryPercentage >= 1:
			# self.testPlus = False
			# self.rpmVal = 2500
		# elif self.batteryPercentage <= 0:
			# self.testPlus = True
			# self.rpmVal = 0
		###################
		
		# Get RPM value
		self.erpmVal = int.from_bytes(self.erpm_buffer, byteorder='big')
		self.rpmVal = int(self.erpmVal / self.pole_pairs)
		# Get Other Value
		tempCurrent = int.from_bytes(self.current_buffer, byteorder='big')
		self.currentVal = float(tempCurrent / 10.0)
		tempWattHrs = int.from_bytes(self.watt_hrs_buffer, byteorder='big')
		self.wattHrsVal = float(tempWattHrs / 10000.0)
		tempWattHrsCharged = int.from_bytes(self.watt_hrs_charged_buffer, byteorder='big')
		self.wattHrsChargedVal = float(tempWattHrsCharged / 10000.0)
		tempVin = int.from_bytes(self.watt_hrs_buffer, byteorder='big')
		self.vinVal = float(tempVin / 10.0)
		self.batteryPercentage = ( ((self.vinVal - 42.0) / 8.2) * 100.0)	# 42V is empty, 50.2V is full. Sohuld be val in range (100.0 - 0.0)
		
		# TEMPORARY - Set battery value for display for e-days
		#self.batteryPercentage = 0.75 
		
		self.rpmChanged.emit(self.rpmVal)
		self.battPercentChanged.emit(self.batteryPercentage)
		self.currentChanged.emit(self.currentVal)
		self.wattHrsChanged.emit(self.wattHrsVal)
		self.wattHrsChargedChanged.emit(self.wattHrsChargedVal)
		self.vinChanged.emit(self.vinVal)


#Control Slots
	@Slot()
	def toggleHeadlight(self):
		self.isHeadlightOn = not(self.isHeadlightOn)
		if self.isHeadlightOn:
			print(">>>>>>>Headlights ON!")
		else:
			print(">>>>>>>Headlights OFF!")


#Information Property Slots
	@Slot(result=str)
	def getSpeed(self):
		# multiply motor rpm by gear ratio
		wheelrpm = (self.rpmVal*9)/30
		# wheel circumference (in miles) and (60 m/h)
		speed = round(wheelrpm * 0.0003866793 * 60)
		return str(speed)
		
	@Slot(result=str)
	def getRPM(self):
		return str(self.rpmVal)

	@Slot(result=str)
	def getBatteryPercent(self):
		return str(self.batteryPercentage)
	
	# Gonna try turing the float into a str
	@Slot(result=str)
	def getCurrentVal(self):
		return str(self.currentVal)
	
	@Slot(result=str)
	def getWattHrs(self):
		return str(self.wattHrsVal)
	
	@Slot(result=str)
	def getWattHrsCharged(self):
		return str(self.wattHrsChargedVal)
	
	@Slot(result=str)
	def getVin(self):
		return str(self.vinVal)


#Direction Property Slots
	@Slot(str)
	def setDirection(self, direction):
		if(self.rpmVal == 0 and not(self.getLocked())):
			self.direction = direction
			self.directionChanged.emit(direction)
			print(">>>>>>>"+direction)

	@Slot(result=bool)
	def getResting(self):
		if(self.rpmVal < 50):
			return True
		else:
			return False

	@Slot(result=bool)
	def getForward(self):
		if(self.direction == "forward"):
			return True
		else:
			return False

	@Slot(result=bool)
	def getReverse(self):
		if(self.direction == "reverse"):
			return True
		else:
			return False

	@Slot(result=bool)
	def getParked(self):
		if(self.direction == "parked"):
			return True
		else:
			return False


#State Property Slots	
	@Slot(str)
	def setState(self, state):
		self.dashState = state
		self.stateChanged.emit(state)
		print(">>>>>>>"+state)

	@Slot(result=str)
	def getState(self):
		return self.dashState

	@Slot(result=bool)
	def getDefault(self):
		return self.dashState == "default"

	@Slot(result=bool)
	def getLocked(self):
		return self.dashState == "locked"


	#Information Properties
	speed = Property(str, getSpeed, notify=rpmChanged)
	rpm = Property(str, getRPM, notify=rpmChanged)
	batteryPercent = Property(str, getBatteryPercent, notify=battPercentChanged)
	current = Property(str, getCurrentVal, notify=currentChanged)
	wattHrs = Property(str, getWattHrs, notify=wattHrsChanged)
	wattHrsCharged = Property(str, getWattHrsCharged, notify=wattHrsChargedChanged)
	vin = Property(str, getVin, notify=vinChanged)

	#Direction Properties
	atRest = Property(bool, getResting, notify=rpmChanged)
	forward = Property(bool, getForward, notify=directionChanged)
	reverse = Property(bool, getReverse, notify=directionChanged)
	parked = Property(bool, getParked, notify=directionChanged)

	#State Properties
	state = Property(str, getState, setState, notify=stateChanged)
	default = Property(bool, getDefault, notify=stateChanged)
	locked = Property(bool, getLocked, notify=stateChanged)
