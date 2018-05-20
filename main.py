import sys
import time
import threading

from picamera import PiCamera
from picamera.array import PiRGBArray

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

class PreviewWindow(QLabel):
	
	def __init__(self, parent, camera):
		super(PreviewWindow, self).__init__(parent)
		# set preview window geometry
		self.resize(640,480)
		
		# announce camera object
		self.camera = camera
		
		# preview state sentinel
		self.preview_state = False
				
	def start_preview_thread(self):
		# start preview pane thread
		self.frames_thread = threading.Thread(target = self.frame_getter)
		self.preview_state = True
		self.frames_thread.start()
		
	def stop_preview_thread(self):
		# set preview state variable to false
		self.preview_state = False
		self.frames_thread.join()
		
	def update_image(self, image):
		self.setPixmap(QPixmap.fromImage(image))
		
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
				
				# send pixmap to update label
				self.update_image(image)
			 
				# clear the stream in preparation for the next frame
				capturestream_array.truncate(0)
				
			elif not self.preview_state:
				break
			
		
class PreviewButton(QPushButton):
	
	def __init__(self, parent):
		super(PreviewButton, self).__init__('Start Preview Feed', parent)
		
		# announce parent to class and set initial button function to start preview
		self.parent = parent
		self.clicked.connect(self.start_preview)
		
	def start_preview(self):
		# start preview thread
		self.parent.previewwindow.start_preview_thread()
		
		# change text and button function
		self.clicked.disconnect()
		self.setText('Stop Preview Feed')
		self.clicked.connect(self.stop_preview)
		
	def stop_preview(self):
		# stop preview thread
		self.parent.previewwindow.stop_preview_thread()
		
		# change text and button function
		self.clicked.disconnect()
		self.setText('Start Preview Feed')
		self.clicked.connect(self.start_preview)
		
class SnapshotButton(QPushButton):
	
	def __init__(self, parent):
		super(SnapshotButton, self).__init__('Take Snapshot', parent)
		
		# announce parent to class and set initial button function to start preview
		self.parent = parent
		self.clicked.connect(self.take_snapshot)
		
	def take_snapshot(self):
		# take time-stamped picture			
		#~ current_time = time.strftime("%Y%m%d_time%H%Ms%S")
		#~ file_name = "Im_"+current_time+".jpg"
		file_name = "Im_2.jpg"
		self.parent.camera.capture(file_name, format="jpeg", use_video_port=False)
			
class MainWindow(QWidget):
	
	def __init__(self):
		super().__init__()
		
		# get PiCamera object
		self.camera = PiCamera()
		self.camera.resolution = (1640, 1232)
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
		self.snapshotbutton = SnapshotButton(self)
		#~ self.cameraselection = QComboBox(self)

		# add widgets to vertical box layout
		sublayout_preview.addWidget(self.previewwindow)
		sublayout_preview.addWidget(self.previewbutton)
		sublayout_preview.addWidget(self.snapshotbutton)
		
		# set sublayout as widget layout
		self.setLayout(sublayout_preview)
		
if __name__ == '__main__':
	
    app = QApplication(sys.argv)

    main = MainWindow()
    
    main.show()

    sys.exit(app.exec_())
