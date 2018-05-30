from datetime import datetime
from picamera import PiCamera
from pathlib import Path
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from threading import Thread, Lock

class Camera(PiCamera):
	
	def __init__(self):
		super(Camera, self).__init__()
		
		# set default resolution
		self.resolution = (640, 480)
		
		# set up timed thread variables (make each variable into list for multiple cameras)
		self.initvar_cameratimer()
		
		# preview state sentinel
		self.preview_state = False
		
		# lock to activate whilst still port in use
		self.piclock = Lock()
		
	def initvar_cameratimer(self):
		#every n seconds
		self.everyN = 0
		
		# for n seconds
		self.forN = 0
		
		# take n pictures
		self.takeN = 0
		
		# with spacing n
		self.withgapN = 0
		
	def capture(self):
		with self.piclock:
			# format filename with date/time stamp values if appropriate
			filename = s'Im_day{timestamp:%Y%m%d}_time{timestamp:%H-%M-%S-%f}.jpg'.format(timestamp=datetime.now())
			
			# use parent method to capture, *bayer and quality only used for JPG formats*
			super(Camera, self).capture(filename, format=self.fn.FileFormat, use_video_port=False, bayer=self.fn.bayerInclude, quality=self.fn.JPGquality)
			
	
