# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        # Connect the tabChanged signal to the slot
        self.ui.tabWidget.currentChanged.connect(self.tab_changed)

    def tab_changed(self, index):
        # Check if the tab being switched to is the "Camera" tab
        if index == self.ui.tabWidget.indexOf(self.ui.oakd):
            print("CAMERA tab was clicked")
            # If it is, display the stereo camera feed
        if index == self.ui.tabWidget.indexOf(self.ui.dash):
            print("DASH tab was clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())