from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon

class SetResolutionDropDown(QComboBox):
	
	# start and stop signals declaration
	sig_start_thread = pyqtSignal()
	sig_stop_thread = pyqtSignal()
	
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
		if (current_resolution[0] == '3'):
			self.setCurrentText('3280x2464 (extra GPU ram must be allocated)')
		else:
			self.setCurrentText(current_resolution)
		
		# connect to resolution changer function
		self.currentTextChanged.connect(self.res_changer)
		
	@pyqtSlot(str)
	def res_changer(self, res_in):
		# in case previewing is on, switch off and wait to give
		# thread time to finish
		restart = False
		if (self.camera.preview_state == True):
			self.sig_stop_thread.emit()
			sleep(0.5)
			restart = True
				
		# change camera resolution, include special case for extra text in '3280...'
		if (res_in[0] == '3'):
			self.camera.resolution = '3280x2464'
			
		else:
			self.camera.resolution = res_in

		# restart preview thread if was on before
		if restart:
			self.sig_start_thread.emit()
			
		print('Succesfully changed resolution to:', self.camera.resolution)	

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
		self.text = QLabel('Resolution:')
		self.dropdown = SetResolutionDropDown(self.camera)
		
		# add widgets to layout
		setres_layout.addWidget(self.text)
		setres_layout.addWidget(self.dropdown)
		
		# set setres_layout as widget layout
		self.setLayout(setres_layout)
		
class SettingsWindow(QDialog):
	
	def __init__(self, parent, camera):
		super(SettingsWindow, self).__init__(parent)
		
		# announce parent (main window)
		self.main_window = parent
		
		# announce camera handle
		self.camera = camera
		
		# initialise user interface
		self.initUI()
		
		# connect signals and slot
		self.sigslot_connector()		
		
	def initUI(self):
		# set title
		self.setWindowTitle('Camera Settings')
		
		# set layout
		settings_layout = QVBoxLayout()
		
		# get widgets
		self.setting_resolution = SetResolution(self.main_window, self.camera)
		
		# add widgets to layout
		settings_layout.addWidget(self.setting_resolution)		
		
		# set settings_layout as widget layout
		self.setLayout(settings_layout)
		
		# set window geometry
		self.setFixedSize(settings_layout.sizeHint())
		
	def sigslot_connector(self):
		# connect capture preview buttons, for change in resolution
		self.setting_resolution.dropdown.sig_start_thread.connect(self.main_window.camerasection.previewwindow.start_preview_thread)
		self.setting_resolution.dropdown.sig_stop_thread.connect(self.main_window.camerasection.previewwindow.stop_preview_thread)

class CameraSettingsButton(QPushButton):
	
	def __init__(self, parent, camera):
		super(CameraSettingsButton, self).__init__(QIcon('resources/settings.svg'), '  Camera Settings', parent)
		
		# announce main window parent and camera
		self.parent = parent
		self.camera = camera
		
		# connect
		self.clicked.connect(self.open_settings)
		
	def open_settings(self):
		# create and open settings window dialog box,
		# with handle on camera object
		settings = SettingsWindow(self.parent, self.camera)
		settings.show()
		
