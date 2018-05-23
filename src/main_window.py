import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication
from src.camerasection import CameraSection
from src.camera import Camera
from src.manualmovement import ManualMovementSection
from src.filemanagement import FileManagementSection

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
		
		# get widgets
		self.camerasection = CameraSection(self, self.camera)
		self.filemanagement = FileManagementSection(self, self.camera)
		self.manualmovement = ManualMovementSection(self, self.camera)
		
		# add widgets to main layout
		mainlayout.addWidget(self.camerasection, 0, 0, 3, 1)
		mainlayout.addWidget(self.filemanagement, 0, 1, 1, 1)
		mainlayout.addWidget(self.manualmovement, 1, 1, 1, 1)

		
		# set mainlayout as widget layout
		self.setLayout(mainlayout)
		
		# set window geometry
		self.setFixedSize(mainlayout.sizeHint())
		self.move(75, 75)
		
	def closeEvent(self, event):
		# ensure preview thread ends
		self.camera.preview_state = False

def run():
	
    app = QApplication(sys.argv)

    main = MainWindow()
    
    main.show()

    sys.exit(app.exec_())

