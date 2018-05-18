import sys
import time

from picamera import PiCamera
from picamera.array import PiRGBArray

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

import RPi.GPIO as GPIO

class PreviewThread(QThread):
	
	# declare Qt signal
	sendPixmap = pyqtSignal(QImage)
	
	def __init__(self, parent, camera):
		super(PreviewThread, self).__init__(parent)
						
		# announce camera variable for run function to use
		self.camera = camera
		
		# preview variable 
		self.preview = True
		
	def stop_preview(self):
		self.preview = False
	
	def run(self):
		
		capturestream_array = PiRGBArray(self.camera, size = (640, 480))
		
		for frame in self.camera.capture_continuous(capturestream_array, format="rgb", resize=(640, 480), use_video_port=True):
			if self.preview:
				
				# grab the image array
				img = frame.array
	
				height, width, bpc = img.shape
				bpl = bpc*width
				image = QImage(img.data, width, height, bpl, QImage.Format_RGB888)
				
				# send pixmap to update label
				self.sendPixmap.emit(image)
			 
				# clear the stream in preparation for the next frame
				capturestream_array.truncate(0)
				
			elif not self.preview:
				break
			
class PreviewWindow(QLabel):
	
	def __init__(self, parent, camera):
		super(PreviewWindow, self).__init__(parent)
		# set preview window geometry
		self.resize(640,480)
		
		# announce camera object
		self.camera = camera
		
		#~ self.start_thread()
		
	def start_thread(self):
		# start preview pane thread
		self.th = PreviewThread(self, self.camera)
		self.th.sendPixmap.connect(self.setImage)
		self.th.start()
		
	def stop_thread(self):
		# stop preview pane thread
		self.th.stop_preview()
		
	@pyqtSlot(QImage)
	def setImage(self, image):
		self.setPixmap(QPixmap.fromImage(image))
		
class PreviewButton(QPushButton):
	
	def __init__(self, parent):
		super(PreviewButton, self).__init__('Start Preview Feed', parent)
		
		self.parent = parent
		
		self.clicked.connect(self.start_preview)
		
	def start_preview(self):
		# start preview thread
		self.parent.previewwindow.start_thread()
		
		# change text and button function
		self.clicked.disconnect()
		self.setText('Stop Preview Feed')
		self.clicked.connect(self.stop_preview)
		
	def stop_preview(self):
		# stop preview thread
		self.parent.previewwindow.stop_thread()
		
		# change text and button function
		self.clicked.disconnect()
		self.setText('Start Preview Feed')
		self.clicked.connect(self.start_preview)
		
class MainWindow(QWidget):
	
	def __init__(self):
		super().__init__()
		
		# get PiCamera object
		self.camera = PiCamera()
		self.camera.framerate = 14
		
		# initialise user interface
		self.initUI()
	
	def initUI(self):
		# general settings
		self.setWindowTitle("Video Feed Test")
		self.setGeometry(50, 50, 640, 580)
		
		# preview section layout
		sublayout_preview = QVBoxLayout()
		
		# initialise widgets
		self.previewwindow = PreviewWindow(self, self.camera)
		self.previewbutton = PreviewButton(self)
		#~ self.cameraselection = QComboBox(self)

		# add widgets to vertical box layout
		sublayout_preview.addWidget(self.previewwindow)
		sublayout_preview.addWidget(self.previewbutton)
		
		# set sublayout as widget layout
		self.setLayout(sublayout_preview)
		
if __name__ == '__main__':
	
    app = QApplication(sys.argv)

    main = MainWindow()
    
    main.show()

    sys.exit(app.exec_())
