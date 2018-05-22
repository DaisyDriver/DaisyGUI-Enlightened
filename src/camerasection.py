import sys
import time
import threading

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage, QIcon

from src.settings import SettingsWindow

class PreviewWindow(QLabel):
	
	def __init__(self, parent, camera):
		super(PreviewWindow, self).__init__(parent)
		# set preview window geometry
		self.resize(640,480)
		
		# announce camera object
		self.camera = camera
		
		# preview state sentinel
		self.preview_state = False
		
		# set no-feed image
		self.goat = QImage('resources/goat-small.jpg')
		self.setPixmap(QPixmap.fromImage(self.goat))
		
		# set frame
		self.setFrameShape(QFrame.Panel)
		self.setLineWidth(1)
		
	@pyqtSlot()	
	def start_preview_thread(self):
		# start preview pane thread
		self.frames_thread = threading.Thread(target = self.frame_getter)
		self.preview_state = True
		self.frames_thread.start()
		
	@pyqtSlot()		
	def stop_preview_thread(self):
		# set preview state variable to false
		self.preview_state = False
		
		# if thread started, wait for it to complete
		self.frames_thread.join()
		
		# set no-feed image
		self.setPixmap(QPixmap.fromImage(self.goat))
		
	def frame_getter(self):
		# set up bit stream for catching frames
		capturestream_array = PiRGBArray(self.camera, size = (640, 480))

		for frame in self.camera.capture_continuous(capturestream_array, format="rgb", resize=(640, 480), use_video_port=True):
			if self.preview_state:
				
				# grab the image array
				img = frame.array
		
				height, width, bpc = img.shape
				bpl = bpc*width
				image = QImage(img.data, width, height, bpl, QImage.Format_RGB888)
				
				# use pixmap to update label (preview pane)
				self.setPixmap(QPixmap.fromImage(image))
			 
				# clear the stream in preparation for the next frame
				capturestream_array.truncate(0)
				
			elif not self.preview_state:
				break
		
class PreviewButton(QPushButton):
	
	# start and stop signals declaration
	sig_start_thread = pyqtSignal()
	sig_stop_thread = pyqtSignal()
	
	def __init__(self, parent):
		super(PreviewButton, self).__init__('Start Preview Feed', parent)
		
		# announce parent to class and set initial button function to start preview
		self.parent = parent
		self.clicked.connect(self.start_preview)
		self.setIcon(QIcon('resources/play.svg'))
		
	def start_preview(self):
		# start preview thread
		self.sig_start_thread.emit()
		
		# change text, icon and button function
		self.clicked.disconnect()
		self.setText('Stop Preview Feed')
		self.clicked.connect(self.stop_preview)
		self.setIcon(QIcon('resources/square.svg'))
		
	def stop_preview(self):
		# stop preview thread
		self.sig_stop_thread.emit()
		
		# change text, icon and button function
		self.clicked.disconnect()
		self.setText('Start Preview Feed')
		self.clicked.connect(self.start_preview)
		self.setIcon(QIcon('resources/play.svg'))
		
class SnapshotButton(QPushButton):
	
	def __init__(self, parent, camera):
		super(SnapshotButton, self).__init__(QIcon('resources/camera.svg'), 'Take Snapshot', parent)
		
		# set initial button function to start preview
		self.clicked.connect(camera.capture)
		
class CameraSettingsButton(QPushButton):
	
	def __init__(self, parent, camera):
		super(CameraSettingsButton, self).__init__(QIcon('resources/settings.svg'), 'Camera Settings', parent)
		
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
		
class CameraSection(QGroupBox):
	
	def __init__(self, parent, camera):
		super(CameraSection, self).__init__(parent)
		
		# get customised PiCamera instance
		self.camera = camera
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# general settings
		self.setTitle('Camera')
		
		# preview section layout
		sublayout_preview = QVBoxLayout()
		
		# initialise widgets
		self.previewwindow = PreviewWindow(self, self.camera)
		self.previewbutton = PreviewButton(self)
		self.snapshotbutton = SnapshotButton(self, self.camera)
		self.settingsbutton = CameraSettingsButton(self, self.camera)
		#~ self.cameraselection = QComboBox(self)

		# add widgets to vertical box layout
		sublayout_preview.addWidget(self.previewwindow)
		sublayout_preview.addWidget(self.previewbutton)
		sublayout_preview.addWidget(self.snapshotbutton)
		sublayout_preview.addWidget(self.settingsbutton)
		
		# set sublayout as widget layout
		self.setLayout(sublayout_preview)
		
		# connect signals to slots
		self.sigslot_connector()
		
	def sigslot_connector(self):
		# connect capture preview buttons
		self.previewbutton.sig_start_thread.connect(self.previewwindow.start_preview_thread)
		self.previewbutton.sig_stop_thread.connect(self.previewwindow.stop_preview_thread)
