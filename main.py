import sys
import time

from picamera import PiCamera
from picamera.array import PiRGBArray

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

class PreviewThread(QThread):
	
	sendPixmap = pyqtSignal(QImage)
	
	def run(self):
		
		camera = PiCamera()
		camera.resolution = (640, 480)
		camera.framerate = 14
		
		rawCapture = PiRGBArray(camera, size = (640, 480))
		
		for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
			# grab the image array
			img = frame.array

			height, width, bpc = img.shape
			bpl = bpc*width
			image = QImage(img.data, width, height, bpl, QImage.Format_RGB888)
			
			# send pixmap to update label
			self.sendPixmap.emit(image)
		 
			# clear the stream in preparation for the next frame
			rawCapture.truncate(0)
			
class PreviewWindow(QLabel):
	
	def __init__(self, parent):
		super(PreviewWindow, self).__init__(parent)
		
		self.resize(640,480)
		
		th = PreviewThread(self)
		th.sendPixmap.connect(self.setImage)
		th.start()
		
	@pyqtSlot(QImage)
	def setImage(self, image):
		self.setPixmap(QPixmap.fromImage(image))

class MainWindow(QWidget):
	
	def __init__(self):
		super().__init__()
		self.initUI()
	
	def initUI(self):
		# general settings
		self.setWindowTitle("Video Feed Test")
		self.setGeometry(50, 50, 640, 580)
		
		# preview section layout
		sublayout_preview = QHBoxLayout()
		
		self.previewwindow = PreviewWindow(self)
		
		#~ self.cameraselection = QComboBox(self)
		
		#~ self.capturebutton = 
		
		sublayout_preview.addWidget(self.previewwindow)

if __name__ == '__main__':
	
    app = QApplication(sys.argv)

    main = MainWindow()
    
    main.show()

    sys.exit(app.exec_())
