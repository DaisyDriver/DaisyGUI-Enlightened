from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class EveryFor(QWidget):
	
	def __init__(self, parent, camera):
		super(EveryFor, self).__init__(parent)
		
		# announce camera
		self.camera = camera
		
		# init UI
		self.initUI()
		
		# connect signals to slots
		
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
		
	#~ def 
		
class TakeWithGap(QWidget):
	
	def __init__(self, parent, camera):
		super(TakeWithGap, self).__init__(parent)
		
		# announce camera
		self.camera = camera
		
		# init UI
		self.initUI()
		
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
		
class TimerStart(QPushButton):
	
	def __init__(self, parent):
		super(TimerStart, self).__init__(QIcon('resources/rocket.svg'), ' Start!', parent)
		
class StopReset(QPushButton):
	
	def __init__(self, parent):
		super(StopReset, self).__init__(QIcon('resources/hand.svg'), ' Stop/Reset', parent)
		
class BottomButtons(QWidget):
	
	def __init__(self, parent, camera):
		super(BottomButtons, self).__init__(parent)
		
		# init UI
		self.initUI()
		
	def initUI(self):
		# sublayout get
		bottombuttons_sublayout = QHBoxLayout()
		
		# get widgets
		self.sreset = StopReset(self)
		self.tstart = TimerStart(self)
		
		# add widgets to sublayout
		bottombuttons_sublayout.addWidget(self.sreset)
		bottombuttons_sublayout.addWidget(self.tstart)
		
		# set sublayout
		self.setLayout(bottombuttons_sublayout)
		
class CameraTimerSection(QGroupBox):
	
	def __init__(self, parent, camera):
		super(CameraTimerSection, self).__init__(parent)
		
		# announce camera handle
		self.camera = camera
		
		# init UI
		self.initUI()
		
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
		

