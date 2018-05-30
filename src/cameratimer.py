from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class EveryFor(QWidget):
	
	# for checking text fields are all non-zero 
	onchangetext = pyqtSignal()
	
	def __init__(self, parent, camera):
		super(EveryFor, self).__init__(parent)
		
		# announce camera
		self.camera = camera
		
		# init UI
		self.initUI()
		
		# connect signals to slots
		self.signalslotconnector()
		
	def initUI(self):
		# set layout
		sublayout_everyfor = QHBoxLayout()
		
		# get widgets
		self.everylabel = QLabel('Every', self)
		self.everytext = QLineEdit(self)
		self.everybox = QComboBox(self)
		self.forlabel = QLabel('for', self)
		self.fortext = QLineEdit(self)
		self.forbox = QComboBox(self)
		
		# edit widgets appearances'
		self.everytext.setFixedWidth(55)
		self.fortext.setFixedWidth(55)
		
		self.everybox.setFixedWidth(90)
		self.everybox.addItem('seconds')
		self.everybox.addItem('minutes')
		
		self.forbox.setFixedWidth(87)
		self.forbox.addItem('minutes')
		self.forbox.addItem('hours')
		
		# add widgets to layout
		sublayout_everyfor.addWidget(self.everylabel)
		sublayout_everyfor.addWidget(self.everytext)
		sublayout_everyfor.addWidget(self.everybox)
		sublayout_everyfor.addWidget(self.forlabel)
		sublayout_everyfor.addWidget(self.fortext)
		sublayout_everyfor.addWidget(self.forbox)
		
		# set sublayout to widget
		self.setLayout(sublayout_everyfor)
		
	@pyqtSlot(str)
	def update_everyN(self, every_in):
		#validate
		valid, number_in = self.verify_input(every_in)
		
		# update if valid
		if valid:
			if self.everybox.currentText() == 'seconds':
				self.camera.everyN = number_in
			
			elif self.everybox.currentText() == 'minutes':
				self.camera.everyN = number_in*60
				
		# emit on text change signal
		self.onchangetext.emit()
	
	@pyqtSlot(str)
	def everyNboxchange(self):
		# get text box value and call updater function
		self.update_everyN(self.everytext.text())
		
	@pyqtSlot(str)
	def update_forN(self, for_in):
		# validate
		valid, number_in = self.verify_input(for_in)
		
		# update if valid
		if valid:
			if self.forbox.currentText() == 'minutes':
				# convert to seconds and set
				self.camera.forN = number_in*60 
			
			elif self.forbox.currentText() == 'hours':
				# convert to seconds and set
				self.camera.forN = number_in*60*60
				
		# emit on text change signal
		self.onchangetext.emit()
	
	@pyqtSlot(str)
	def forNboxchange(self):
		# get text box value and call updater function
		self.update_forN(self.fortext.text())		

	def signalslotconnector(self):
		# connect every text box and combo box
		self.everytext.textEdited.connect(self.update_everyN)
		self.everybox.currentTextChanged.connect(self.everyNboxchange)
		
		# connect for text box and combo box
		self.fortext.textEdited.connect(self.update_forN)
		self.forbox.currentTextChanged.connect(self.forNboxchange)
		
	def verify_input(self, text_in):
		# check for validity of input
		validchars = '0123456789'
		
		if not all([char in validchars for char in text_in]):
			error_dialog = QMessageBox.critical(self, 'Incorrect number input', 
												'Input number must be an integer between 1 and 1000 inclusive',
												QMessageBox.Ok)
			return (False, 0)
			
		elif len(text_in)==0:
			
			return (True, 0)
		
		number_in = int(text_in)
		
		if number_in<1:
			error_dialog = QMessageBox.critical(self, 'Incorrect number input', 
												'Input number must be an integer between 1 and 1000 inclusive',
												QMessageBox.Ok)
			return (False, 0)
		
		elif number_in>1000:
			error_dialog = QMessageBox.critical(self, 'Incorrect number input', 
									'Input number must be an integer between 1 and 1000 inclusive',
									QMessageBox.Ok)
			return (False, 0)
			
		else:
			return (True, number_in)
		
class TakeWithGap(QWidget):
	
	# for checking text fields are all non-zero 
	onchangetext = pyqtSignal()
	
	def __init__(self, parent, camera):
		super(TakeWithGap, self).__init__(parent)
		
		# announce camera
		self.camera = camera
		
		# init UI
		self.initUI()
		
		# connect signals and slots
		self.signalslotconnector()
		
	def initUI(self):
		# set layout
		sublayout_takewithgap = QHBoxLayout()
		
		# get widgets
		self.takelabel = QLabel('take', self)
		self.taketext = QLineEdit(self)
		self.gaplabel = QLabel('pictures, with spacing of', self)
		self.gaptext = QLineEdit(self)
		self.gaplabel2 = QLabel('seconds.', self)
		
		# edit widgets appearances'
		self.taketext.setFixedWidth(41)
		self.gaptext.setFixedWidth(41)
		
		# add widgets to layout
		sublayout_takewithgap.addWidget(self.takelabel)
		sublayout_takewithgap.addWidget(self.taketext)
		sublayout_takewithgap.addWidget(self.gaplabel)
		sublayout_takewithgap.addWidget(self.gaptext)
		sublayout_takewithgap.addWidget(self.gaplabel2)
		
		# set widget layout
		self.setLayout(sublayout_takewithgap)
		
	@pyqtSlot(str)
	def update_takeN(self, take_in):
		#validate
		valid, number_in = self.verify_input(take_in)
		
		# update if valid
		if valid:
			self.camera.takeN = number_in
			
		# emit on text change signal
		self.onchangetext.emit()
		
		# special case for only taking 1 picture (no gap)
		if number_in == 1:
			self.gaptext.setEnabled(False)
		else:
			self.gaptext.setEnabled(True)
			
	@pyqtSlot(str)
	def update_withgapN(self, gap_in):
		#validate
		valid, number_in = self.verify_input(gap_in)
		
		# update if valid
		if valid:
			self.camera.withgapN = number_in
			
		# emit on text change signal
		self.onchangetext.emit()
		
	def signalslotconnector(self):
		# connect take text box
		self.taketext.textEdited.connect(self.update_takeN)
		
		# connect with spacing text box
		self.gaptext.textEdited.connect(self.update_withgapN)
		
	def verify_input(self, text_in):
		# check for validity of input
		validchars = '0123456789'
		
		if not all([char in validchars for char in text_in]):
			error_dialog = QMessageBox.critical(self, 'Incorrect number input', 
												'Input number must be an integer greater than or equal to 1',
												QMessageBox.Ok)
			return (False, 0)
			
		elif len(text_in)==0:
			
			return (True, 0)
		
		number_in = int(text_in)
		
		if number_in<1:
			error_dialog = QMessageBox.critical(self, 'Incorrect number input', 
												'Input number must be an integer greater than or equal to 1',
												QMessageBox.Ok)
			return (False, 0)
			
		else:
			return (True, number_in)
		
class TimerStart(QPushButton):
	
	enablestop = pyqtSignal()
	
	def __init__(self, parent, camera):
		super(TimerStart, self).__init__(QIcon('resources/rocket.svg'), ' Start!', parent)
		
		# announce camera
		self.camera = camera
		
		# set disabled initially
		self.setEnabled(False)
		
		# connect clicked
		self.clicked.connect(self.onclick)
		
	@pyqtSlot()
	def ontextchange(self):
		# check all values are non-zero and enable if so, disable if not
		cameratimer_vars = [self.camera.everyN,
							self.camera.forN,
							self.camera.takeN,
							self.camera.withgapN]
		
		# general case
		if all(value != 0 for value in cameratimer_vars):
			self.setEnabled(True)
		# special case of only taking 1 picture (gap irrelevant)
		elif self.camera.takeN == 1 and self.camera.everyN != 0 and self.camera.forN != 0:
			self.setEnabled(True)
		else:
			self.setEnabled(False)
			
	@pyqtSlot()
	def onclick(self):
		# check picture taking sequence is less time than gap between sequences
		sequence_time = self.camera.takeN*self.camera.withgapN
		if sequence_time < self.camera.everyN or self.camera.takeN == 1:
			# disable start button and enable stop/reset button
			self.setEnabled(False)
			self.enablestop.emit()
			
			# start timed picture sequence!
			self.camera.start_timed_capture()
			
		else:
			error_dialog = QMessageBox.critical(self, 'Incorrect number input', 
									'Picture taking sequence must take less time than gap between sequences',
									QMessageBox.Ok)
									
	@pyqtSlot()
	def onstop(self):
		# on stop, re-enable start button
		self.setEnabled(True)

class StopReset(QPushButton):
	
	enablestart = pyqtSignal()
	
	def __init__(self, parent, camera):
		super(StopReset, self).__init__(QIcon('resources/hand.svg'), ' Stop/Reset', parent)
		
		# announce camera
		self.camera = camera
		
		# set disabled initially
		self.setEnabled(False)
		
		# connect to onclicked
		self.clicked.connect(self.onclicked)
		
	@pyqtSlot()
	def onstart(self):
		# once timer started, enable button
		self.setEnabled(True)
		
	@pyqtSlot()
	def onclicked(self):
		# stop timer, disable stop button and re-enable start button
		self.camera.stop_timed_capture()
		self.setEnabled(False)
		self.enablestart.emit()
		
	@pyqtSlot()
	def onfinish(self):
		self.setEnabled(False)
		self.enablestart.emit()
		
class BottomButtons(QWidget):
	
	def __init__(self, parent, camera):
		super(BottomButtons, self).__init__(parent)
		
		# announce camera
		self.camera = camera
		
		# init UI
		self.initUI()
		
		# connect signals and slots
		self.signalslotconnector()
		
	def initUI(self):
		# sublayout get
		bottombuttons_sublayout = QHBoxLayout()
		
		# get widgets
		self.sreset = StopReset(self, self.camera)
		self.tstart = TimerStart(self, self.camera)
		
		# add widgets to sublayout
		bottombuttons_sublayout.addWidget(self.sreset)
		bottombuttons_sublayout.addWidget(self.tstart)
		
		# set sublayout
		self.setLayout(bottombuttons_sublayout)
		
	def signalslotconnector(self):
		# connect start timer button to enable stop button
		self.tstart.enablestop.connect(self.sreset.onstart)
		# connect stop timer button to enable start button
		self.sreset.enablestart.connect(self.tstart.onstop)

		
class CameraTimerSection(QGroupBox):
	
	def __init__(self, parent, camera):
		super(CameraTimerSection, self).__init__(parent)
		
		# announce camera handle
		self.camera = camera
		
		# init UI
		self.initUI()
		
		# connect signals and slots
		self.signalslotconnector()
		
	def initUI(self):
		# general settings
		self.setTitle('Camera Timer')
		
		# section layout
		sublayout_cameratimer = QVBoxLayout()
		
		# initialise widgets
		self.everyfor = EveryFor(self, self.camera)
		self.takewith = TakeWithGap(self, self.camera)
		self.BB = BottomButtons(self, self.camera)

		# add widgets to vertical box layout
		sublayout_cameratimer.addWidget(self.everyfor)
		sublayout_cameratimer.addWidget(self.takewith)
		sublayout_cameratimer.addWidget(self.BB)
		
		# set smaller spacing
		sublayout_cameratimer.setSpacing(1)

		# set sublayout as widget layout
		self.setLayout(sublayout_cameratimer)
		
		# set geometry
		#~ self.setFixedSize(sublayout_fileman.sizeHint())
		
	def signalslotconnector(self):
		# connect everyfor changetext signal to start button
		self.everyfor.onchangetext.connect(self.BB.tstart.ontextchange)
		# connect takewith changetext signal to start button
		self.takewith.onchangetext.connect(self.BB.tstart.ontextchange)
		

