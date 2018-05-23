from datetime import datetime
from picamera import PiCamera
from pathlib import Path

class Camera(PiCamera):
	
	def __init__(self):
		super(Camera, self).__init__()
		
		# set default resolution
		self.resolution = (1640, 1232)
		
		# set default save directory, make folder if does not exist
		self.savedir = '/home/pi/DaisyGUI/'
		Path(self.savedir).mkdir(parents=True, exist_ok=True) 
		
		# preview state sentinel
		self.preview_state = False
		
		# set default file format
		self.fileformat = 'jpeg'
		
		# set default name format
		self.nameformat = 'Image{timestamp:_day%Y%m%d_time%H-%M-%S-%f}.jpg'
		
	def capture(self):
		# get time/date signature
		file_name = self.savedir + self.nameformat.format(timestamp=datetime.now())
		
		# use parent method to capture
		super(Camera, self).capture(file_name, format=self.fileformat, use_video_port=False)
		
