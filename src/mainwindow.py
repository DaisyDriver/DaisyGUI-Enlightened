import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication
from src.camerasection import CameraSection
from src.camera import Camera
from src.manualmovement import ManualMovementSection
from src.filemanagement import FileManagementSection
from src.motorbackend import DaisyDriver
from src.cameratimer import CameraTimerSection

class MainWindow(QWidget):
	
	def __init__(self):
		super().__init__()
		
		# get customised PiCamera instance
		self.camera = Camera()
		
		# get daisy driver object
		self.DD = DaisyDriver()
		
		# initialise user interface
		self.initUI()
	
	def initUI(self):
		# general settings
		self.setWindowTitle('DaisyGUI v0.7')
		
		# main layout
		mainlayout = QGridLayout()
		
		# get widgets
		self.camerasection = CameraSection(self, self.camera)
		self.filemanagement = FileManagementSection(self, self.camera)
		self.manualmovement = ManualMovementSection(self, self.camera, self.DD)
		self.cameratimer = CameraTimerSection(self, self.camera)
		
		# add widgets to main layout
		mainlayout.addWidget(self.camerasection, 0, 0, 3, 1)
		mainlayout.addWidget(self.filemanagement, 0, 1, 1, 1)
		mainlayout.addWidget(self.manualmovement, 1, 1, 1, 1)
		mainlayout.addWidget(self.cameratimer, 2, 1, 1, 1)

		# set mainlayout as widget layout
		self.setLayout(mainlayout)
		
		# set window geometry
		self.setFixedSize(mainlayout.sizeHint())
		self.move(75, 75)
		
	def closeEvent(self, event):
		# ensure preview thread ends
		self.camera.preview_state = False
		# ensure close daisy driver serial object
		self.DD.close()

def run():
	
    app = QApplication(sys.argv)

    main = MainWindow()
    
    main.show()

    sys.exit(app.exec_())

