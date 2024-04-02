import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtMultimediaWidgets import QCameraViewfinder
from PySide6.QtMultimedia import QCamera, QCameraInfo

from ui_form import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Find available cameras
        camera_info = QCameraInfo.availableCameras()
        
        if camera_info:
            # Create a camera object
            self.camera = QCamera(camera_info[0])

            # Create a layout for the camera widget
            self.camera_layout = QVBoxLayout()
            self.camera_viewfinder = QCameraViewfinder()
            self.camera_layout.addWidget(self.camera_viewfinder)

            # Add camera viewfinder to the oakd tab
            self.ui.oakd.setLayout(self.camera_layout)

            # Set camera viewfinder
            self.camera.setViewfinder(self.camera_viewfinder)
            self.camera.start()

        else:
            # If no camera found, show a label indicating it
            no_camera_label = QLabel("No camera found")
            self.ui.oakd.layout().addWidget(no_camera_label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
