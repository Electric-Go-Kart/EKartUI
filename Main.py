import sys
from PySide6.QtGui import QGuiApplication, QFontDatabase
from PySide6.QtQml import QQmlApplicationEngine
import lib.DashboardController
import lib.APDView
from PySide6.QtCore import QObject, Slot
from your_gpio_controller_module import GPIOController
	
app = QGuiApplication([])
engine = QQmlApplicationEngine()

gpioController = GPIOController()
engine.rootContext().setContextProperty("gpioController", gpioController)

QFontDatabase.addApplicationFont("ui/fonts/Royal_Rumble_Haettenschweiler.ttf")
engine.load("ui/Main.qml")

if not engine.rootObjects():
	sys.exit(-1)
sys.exit(app.exec())
