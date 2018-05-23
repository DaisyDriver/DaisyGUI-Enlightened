from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class ManMoveZ(QGroupBox):
	
	def __init__(self, parent):
		super(ManMoveZ, self).__init__(parent)
		
		# announce parent
		self.parent = parent
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# general settings
		self.setTitle('Z plane')
		
		# XY controls, grid layout
		sublayout_Z = QGridLayout()
		
		# initialise widgets
		self.up = QPushButton(QIcon('resources/arrowup.svg'), '', self.parent)
		self.down = QPushButton(QIcon('resources/arrowdown.svg'), '', self.parent)
		
		# add widgets to vertical box layout
		sublayout_Z.addWidget(self.up, 0, 0, 1, 1)
		sublayout_Z.addWidget(self.down, 2, 0, 1, 1)
		
		# set sublayout as widget layout
		self.setLayout(sublayout_Z)
		
		# set geometry
		self.setFixedSize(85, 175)

class ManMoveXY(QGroupBox):
	
	def __init__(self, parent):
		super(ManMoveXY, self).__init__(parent)
		
		# announce parent
		self.parent = parent
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# general settings
		self.setTitle('X/Y plane')
		
		# XY controls, grid layout
		sublayout_XY = QGridLayout()
		
		# initialise widgets
		self.left = QPushButton(QIcon('resources/bubble_left.svg'), '', self.parent)
		self.right = QPushButton(QIcon('resources/bubble_right.svg'), '', self.parent)
		self.up = QPushButton(QIcon('resources/bubble_up.svg'), '', self.parent)
		self.upright = QPushButton(QIcon('resources/bubble_upright.svg'), '', self.parent)
		self.upleft = QPushButton(QIcon('resources/bubble_upleft.svg'), '', self.parent)
		self.down = QPushButton(QIcon('resources/bubble_down.svg'), '', self.parent)
		self.downright = QPushButton(QIcon('resources/bubble_downright.svg'), '', self.parent)
		self.downleft = QPushButton(QIcon('resources/bubble_downleft.svg'), '', self.parent)
		
		# set size
		self.left.setFixedSize(40, 40)
		self.right.setFixedSize(40, 40)
		self.up.setFixedSize(40, 40)
		self.upright.setFixedSize(40, 40)
		self.upleft.setFixedSize(40, 40)
		self.down.setFixedSize(40, 40)
		self.downright.setFixedSize(40, 40)
		self.downleft.setFixedSize(40, 40)
		
		# change buttons to square!!
		
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
		self.setFixedSize(150, 175) # MAKE this SQUARE!!

class ManualMovementSection(QGroupBox):
	
	def __init__(self, parent, camera):
		super(ManualMovementSection, self).__init__(parent)
		
		# announce parent (main window)
		self.main_window = parent
		
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
		self.manXY= ManMoveXY(self)
		self.manZ = ManMoveZ(self)

		# add widgets to vertical box layout
		sublayout_manmove.addWidget(self.manXY)
		sublayout_manmove.addWidget(self.manZ)

		# set sublayout as widget layout
		self.setLayout(sublayout_manmove)


