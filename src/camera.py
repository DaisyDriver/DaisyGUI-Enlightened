from datetime import datetime
from picamera import PiCamera
from pathlib import Path
from PyQt5.QtCore import pyqtSignal, QObject
from threading import Lock, Thread
from src.cameratimerbackend import RepeatedTimer

from time import sleep

class FileNameHelper():
	
	def __init__(self):
		# set default save directory, make folder if does not exist
		self.savedir = '/home/pi/DaisyGUI/'
		Path(self.savedir).mkdir(parents=True, exist_ok=True)
		
		# set default name and file format
		self.NamePrefix = 'Im'
		self.DateStamp = True
		self.TimeStamp = True
		self.FileFormat = 'jpeg'
		self.filenamehelper(self.NamePrefix, self.DateStamp, self.TimeStamp, self.FileFormat)
		
		# for custom file names, add default format programatically
		self.custombool = False
		self.customname = 'Im_day{timestamp:%Y%m%d}_time{timestamp:%H-%M-%S-%f}'
				
		# jpg format settings
		self.bayerInclude = True
		self.JPGquality = 100
		
	def filenameswitcher(self):
		# for turning custom name on/off
		if self.custombool:
			self.filename_unformat = self.customname + '.' + self.FileFormat
		elif not self.custombool:
			self.filenamehelper(self.NamePrefix, self.DateStamp, self.TimeStamp, self.FileFormat)
		
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
		
class CallBackEmitter(QObject):
	
	# timer finished signal
	timer_finished_signal = pyqtSignal()
	
	def __init__(self):
		super(CallBackEmitter, self).__init__()

class Camera(PiCamera):
	
	def __init__(self):
		super(Camera, self).__init__()
		
		# set up camera hardware variables
		self.initvar_camerahardware()
		
		# set up timed thread variables (make each variable into list for multiple cameras)
		self.initvar_cameratimer()
		
		# preview state sentinel
		self.preview_state = False
		
		# get filename object
		self.fn = FileNameHelper()
		
		# lock to activate whilst still port in use
		self.piclock = Lock()
		
		# get callback emitter instance
		self.callbackemitter = CallBackEmitter()
		
	def initvar_camerahardware(self):
		# set default resolution
		self.resolution = (1640, 1232)
		
		# turn off de-noiser for still and video images
		self.image_denoise = False
		self.video_denoise = False
		
		# ensure saturation turned off
		self.saturation = 0
		
		# auto-white balance, starts auto
		self.awb_mode = 'auto'
		
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
			filename = self.fn.savedir + self.fn.filename_unformat.format(timestamp=datetime.now())
			
			# use parent method to capture, *bayer and quality only used for JPG formats*
			super(Camera, self).capture(filename, format=self.fn.FileFormat, use_video_port=False, bayer=self.fn.bayerInclude, quality=self.fn.JPGquality)
			
	def start_timed_capture(self):
		# special case for only 1 picture
		if self.takeN == 1:
			# init main time
			self.maintimer = RepeatedTimer(self.everyN, self.capture, timelimit = self.forN, callback = self.callbackemitter.timer_finished_signal.emit)
			
		else:
			# init camera capture (short time scale) timer
			self.cameratimer = RepeatedTimer(self.withgapN, self.capture, countlimit = self.takeN)
			# init longer time scale timer
			self.maintimer = RepeatedTimer(self.everyN, self.cameratimer.start_all, timelimit = self.forN, callback = self.callbackemitter.timer_finished_signal.emit)
		
		# get thread and start
		self.timedcapturethread = Thread(target = self.maintimer.start_all)
		self.timedcapturethread.start()
		
	def stop_timed_capture(self):
		# stop timed capture, timer may not be running so have to try/except
		try:
			self.maintimer.stop()
		except AttributeError:
			pass
			
		try:
			self.cameratimer.stop()
		except AttributeError:
			pass
			
		self.timedcapturethread.join()
		print('Timer thread succesfully stopped.')
		print(self.timedcapturethread.isAlive())
