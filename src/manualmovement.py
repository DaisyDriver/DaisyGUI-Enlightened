from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import pyqtSignal

class ManMoveSpeed(QGroupBox):
	
	def __init__(self, parent, daisydriver):
		super(ManMoveSpeed, self).__init__(parent)
		
		# announce parent
		self.parent = parent
		
		# announce daisy driver
		self.DD = daisydriver
		
		# initialise user interface
		self.initUI()
		
		# connect slider to daisy driver speed change function
		self.speedslider.valueChanged.connect(self.DD.speedset)
		
	def initUI(self):
		# general settings
		self.setTitle('Speed')
		
		# XY controls, grid layout
		sublayout_speed = QGridLayout()
		
		# initialise widgets
		self.speedslider = QSlider(Qt.Vertical, self.parent)
		self.speedslider.setMinimum(0)
		self.speedslider.setMaximum(2)
		self.speedslider.setTickPosition(QSlider.TicksLeft)
		self.speedslider.setTickInterval(1)
		self.speedslider.setFixedHeight(115)
		self.speedslider.setValue(self.DD.speedval)

		self.hispeed = QLabel('High')
		self.medspeed = QLabel('Med')
		self.lospeed = QLabel('Low')
		
		# add widgets to vertical box layout
		sublayout_speed.addWidget(self.speedslider, 0, 1, 7, 1)
		sublayout_speed.addWidget(self.hispeed, 0, 0, 1, 1)
		sublayout_speed.addWidget(self.medspeed, 3, 0, 1, 1)
		sublayout_speed.addWidget(self.lospeed, 6, 0, 1, 1)
		
		# set sublayout as widget layout
		self.setLayout(sublayout_speed)
		
		# set geometry
		self.setFixedSize(85, 175)
		
class XYbutton(QPushButton):
	
	def __init__(self, icon, parent, daisydriver, direction):
		super(XYbutton, self).__init__(icon, '', parent)
		
		# announce daisydriver
		self.DD = daisydriver
		
		# announce direction
		self.direction = direction
		
		# set geometry
		self.setFixedSize(40, 40)
		
		# connect click
		self.pressed.connect(self.on_click)
		
	def on_click(self):
		# on click send jog info to daisydriver object
		self.DD.jog(self.direction, self)
		
class ManMoveXY(QGroupBox):
	
	def __init__(self, parent, daisydriver):
		super(ManMoveXY, self).__init__(parent)
		
		# announce parent
		self.parent = parent
		
		# announce daisydriver
		self.DD = daisydriver
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# general settings
		self.setTitle('X/Y plane')
		
		# XY controls, grid layout
		sublayout_XY = QGridLayout()
		
		# initialise widgets
		self.left = XYbutton(QIcon('resources/bubble_left.svg'), self.parent, self.DD, 'l')
		self.right = XYbutton(QIcon('resources/bubble_right.svg'), self.parent, self.DD, 'r')
		self.up = XYbutton(QIcon('resources/bubble_up.svg'), self.parent, self.DD, 'f')
		self.upright = XYbutton(QIcon('resources/bubble_upright.svg'), self.parent, self.DD, 'fr')
		self.upleft = XYbutton(QIcon('resources/bubble_upleft.svg'), self.parent, self.DD, 'fl')
		self.down = XYbutton(QIcon('resources/bubble_down.svg'), self.parent, self.DD, 'b')
		self.downright = XYbutton(QIcon('resources/bubble_downright.svg'), self.parent, self.DD, 'br')
		self.downleft = XYbutton(QIcon('resources/bubble_downleft.svg'), self.parent, self.DD, 'bl')
		
		# add widgets to vertical box layout
		sublayout_XY.addWidget(self.left, 1, 0, 1, 1)
		sublayout_XY.addWidget(self.right, 1, 2, 1, 1)
		sublayout_XY.addWidget(self.up, 0, 1, 1, 1)
		sublayout_XY.addWidget(self.upright, 0, 2, 1, 1)
		sublayout_XY.addWidget(self.upleft, 0, 0, 1, 1)
		sublayout_XY.addWidget(self.down, 2, 1, 1, 1)
		sublayout_XY.addWidget(self.downright, 2, 2, 1, 1)
		sublayout_XY.addWidget(self.downleft, 2, 0, 1, 1)
		
		# set sublayout as widget layout
		self.setLayout(sublayout_XY)
		
		# set geometry
		self.setFixedSize(150, 175)
		
class Zbutton(QPushButton):
	
	def __init__(self, icon, parent, daisydriver, direction):
		super(Zbutton, self).__init__(icon, '', parent)
		
		# announce daisydriver
		self.DD = daisydriver
		
		# announce direction
		self.direction = direction
		
		# set geometry
		self.setFixedSize(40, 58)
		self.setIconSize(QSize(23, 23))
		
		# connect click
		self.pressed.connect(self.on_click)
		
	def on_click(self):
		# on click send jog info to daisydriver object
		self.DD.jog(self.direction, self)

class ManMoveZ(QGroupBox):
	
	def __init__(self, parent, daisydriver):
		super(ManMoveZ, self).__init__(parent)
		
		# announce parent
		self.parent = parent
		
		# announce daisydriver
		self.DD = daisydriver
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# general settings
		self.setTitle('Z plane')
		
		# XY controls, grid layout
		sublayout_Z = QGridLayout()
		
		# initialise widgets
		self.up = Zbutton(QIcon('resources/arrowup.svg'), self.parent, self.DD, 'u')
		self.down = Zbutton(QIcon('resources/arrowdown.svg'), self.parent, self.DD, 'd')
		
		# add widgets to vertical box layout
		sublayout_Z.addWidget(self.up, 0, 0, 2, 1)
		sublayout_Z.addWidget(self.down, 2, 0, 2, 1)
		
		# set sublayout as widget layout
		self.setLayout(sublayout_Z)
		
		# set geometry
		self.setFixedSize(85, 175)

class ManualMovementSection(QGroupBox):
	
	def __init__(self, parent, camera, daisydriver):
		super(ManualMovementSection, self).__init__(parent)
		
		# announce parent (main window)
		self.main_window = parent
		
		# announce daisy driver handle
		self.DD = daisydriver
		
		# get customised PiCamera instance (need to know which camera/motors?)
		self.camera = camera
		
		# initialise user interface
		self.initUI()

	def initUI(self):
		# general settings
		self.setTitle('Manual Movement')
		
		# section layout
		sublayout_manmove = QHBoxLayout()
		
		# initialise widgets
		self.manSpeed = ManMoveSpeed(self, self.DD)
		self.manXY= ManMoveXY(self, self.DD)
		self.manZ = ManMoveZ(self, self.DD)

		# add widgets to vertical box layout
		sublayout_manmove.addWidget(self.manSpeed)
		sublayout_manmove.addWidget(self.manXY)
		sublayout_manmove.addWidget(self.manZ)

		# set sublayout as widget layout
		self.setLayout(sublayout_manmove)


