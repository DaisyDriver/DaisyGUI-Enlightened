import sys

from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication

from src.camerasection import CameraSection
from src.camera import Camera

class MainWindow(QWidget):
	
	def __init__(self):
		super().__init__()
		
		# get customised PiCamera instance
		self.camera = Camera()
		
		# initialise user interface
		self.initUI()
	
	def initUI(self):
		# general settings
		self.setWindowTitle('ScopeControl v0.1')
		
		# main layout
		mainlayout = QGridLayout()
		
		# get camerasetup widget
		self.camerasection = CameraSection(self, self.camera)
		
		# add widgets to main layout
		mainlayout.addWidget(self.camerasection, 0,0,1,1)
		
		# set window geometry
		self.setFixedSize(mainlayout.sizeHint())
		self.move(50, 50)
		
	def closeEvent(self, event):
		# ensure preview thread ends
		self.camerasection.previewwindow.preview_state = False

def run():
	
    app = QApplication(sys.argv)

    main = MainWindow()
    
    main.show()

    sys.exit(app.exec_())

