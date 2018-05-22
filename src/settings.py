from time import sleep

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage, QIcon

class SetResolutionDropDown(QComboBox):
	
	def __init__(self, camera):
		super(SetResolutionDropDown, self).__init__()

		# announce camera handle
		self.camera = camera
				
		# initialise box items
		self.initbox()
						
	def initbox(self):
		
		# available choice of resolutions
		self.addItem('3280x2464 (extra GPU ram must be allocated)')
		self.addItem('1640x1232')
		self.addItem('1640x922')
		self.addItem('1280x720')
		self.addItem('1920x1080')
		self.addItem('640x480')
		
		# set to currently chosen resolution
		current_resolution = str(self.camera.resolution)
		self.setCurrentText(current_resolution)
		
		# connect to resolution changer function
		self.currentTextChanged.connect(self.res_changer)
		
	@pyqtSlot(str)
	def res_changer(self, res_in):
		# in case previewing is on, switch off and wait to give
		# thread time to finish
		self.camera.preview_state = False
		sleep(1.5)
		
		# change camera resolution
		try:
			self.camera.resolution = res_in
		finally:
			print('Resolution change succesful')
		
		#~ if not self.running and self.camCheck(scopeSelectIn):
				#~ self.activeCam = scopeSelectIn
		#~ elif self.running:
			#~ self.feedDrop.setCurrentIndex(self.activeCam)
			#~ QMessageBox.warning(self, "Invalid Command", "Warning: Cannot change microscope whilst feed is active.")

class SetResolution(QWidget):
	
	def __init__(self, parent, camera):
		super(SetResolution, self).__init__(parent)
		
		# announce camera handle
		self.camera = camera
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# set layout
		setres_layout = QHBoxLayout()
		
		# get widgets
		self.text = QLabel('Resolution')
		self.dropdown = SetResolutionDropDown(self.camera)
		
		# add widgets to layout
		setres_layout.addWidget(self.text)
		setres_layout.addWidget(self.dropdown)
		
		# set setres_layout as widget layout
		self.setLayout(setres_layout)		

class SettingsWindow(QDialog):
	
	def __init__(self, parent, camera):
		super(SettingsWindow, self).__init__(parent)
		
		# announce camera handle
		self.camera = camera
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# set title
		self.setWindowTitle('Camera Settings')
		
		# set layout
		settings_layout = QVBoxLayout()
		
		# get widgets
		self.setting_resolution = SetResolution(self, self.camera)
		
		# add widgets to layout
		settings_layout.addWidget(self.setting_resolution)		
		
		# set settings_layout as widget layout
		self.setLayout(settings_layout)	

		
