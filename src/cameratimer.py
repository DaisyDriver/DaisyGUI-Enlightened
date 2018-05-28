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
		
class TakeWithGap(QWidget):
	
	def __init__(self, parent, camera):
		super(TakeWithGap, self).__init__(parent)
		
		# announce camera
		self.camera = camera
		
		# init UI
		self.initUI
		
	def initUI(self):
		# set layout
		sublayout_takewithgap = QHBoxLayout()
		
		# get widgets
		

		
		

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

		# add widgets to vertical box layout
		sublayout_cameratimer.addWidget(self.everyfor)

		# set sublayout as widget layout
		self.setLayout(sublayout_cameratimer)
		
		# set geometry
		#~ self.setFixedSize(sublayout_fileman.sizeHint())
		

