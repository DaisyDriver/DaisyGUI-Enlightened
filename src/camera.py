from datetime import datetime
from picamera import PiCamera
from pathlib import Path
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class Camera(PiCamera):
	
	def __init__(self):
		super(Camera, self).__init__()
		
		# set up camera hardware variables
		self.camerasetup_DInit()
		
		# set default save directory, make folder if does not exist
		self.savedir = '/home/pi/DaisyGUI/'
		Path(self.savedir).mkdir(parents=True, exist_ok=True)
		
		# set default name and file format
		self.NamePrefix = 'Im'
		self.DateStamp = True
		self.TimeStamp = True
		self.FileFormat = 'jpeg'
		self.filenamehelper(self.NamePrefix, self.DateStamp, self.TimeStamp, self.FileFormat)
		
		# preview state sentinel
		self.preview_state = False
		
		# jpg format settings
		self.bayerInclude = True
		self.JPGquality = 100
		
	def camerasetup_DInit(self):
		# set default resolution
		self.resolution = (1640, 1232)
		
		# turn off de-noiser for still and video images
		self.image_denoise = False
		self.video_denoise = False
		
		# ensure saturation turned off
		self.saturation = 0
		
		# auto-white balance, starts auto
		self.awb_mode = 'auto'
		
	def filenamehelper(self, prefix, Date, Time, Fformat):
		
		# init file name
		filename_unformat = prefix
		
		# add data and time stamp according to preference
		if Date:
			filename_unformat = filename_unformat + '_day{timestamp:%Y%m%d}'
			
		if Time:
			filename_unformat = filename_unformat + '_time{timestamp:%H-%M-%S-%f}'
			
		# add file format	
		self.filename_unformat = filename_unformat + '.' + Fformat
		
	def filenameSetPrefix(self, Prefix_in):
		# update date stamp status and name accordingly
		self.NamePrefix = Prefix_in
		self.filenamehelper(self.NamePrefix, self.DateStamp, self.TimeStamp, self.FileFormat)
		
	def filenameSetFormat(self, Fformat_in):
		# update file format and name accordingly
		self.FileFormat = Fformat_in
		self.filenamehelper(self.NamePrefix, self.DateStamp, self.TimeStamp, self.FileFormat)
		
	def filenameSetDate(self, DateBool_in):
		# update date stamp status and name accordingly
		self.DateStamp = DateBool_in
		self.filenamehelper(self.NamePrefix, self.DateStamp, self.TimeStamp, self.FileFormat)
		
	def filenameSetTime(self, TimeBool_in):
		# update time stamp status and name accordingly
		self.TimeStamp = TimeBool_in
		self.filenamehelper(self.NamePrefix, self.DateStamp, self.TimeStamp, self.FileFormat)
		
	def capture(self):
		# format filename with date/time stamp values if appropriate
		filename = self.savedir + self.filename_unformat.format(timestamp=datetime.now())
		
		# use parent method to capture, *bayer and quality only used for JPG formats*
		super(Camera, self).capture(filename, format=self.FileFormat, use_video_port=False, bayer=self.bayerInclude, quality=self.JPGquality)
		
