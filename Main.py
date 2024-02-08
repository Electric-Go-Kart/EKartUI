import sys
from PySide6.QtGui import QGuiApplication, QFontDatabase
from PySide6.QtQml import QQmlApplicationEngine
import lib.controllers.DashboardController
import lib.APDView
	
app = QGuiApplication([])
engine = QQmlApplicationEngine()

QFontDatabase.addApplicationFont("ui/fonts/Royal_Rumble_Haettenschweiler.ttf")
engine.load("ui/Main.qml")

if not engine.rootObjects():
	sys.exit(-1)
sys.exit(app.exec())
