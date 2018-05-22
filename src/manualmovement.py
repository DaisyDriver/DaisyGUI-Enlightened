from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage, QIcon

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
		self.setFixedSize(85, 150)

class ManMoveXY(QGroupBox):
	
	def __init__(self, parent):
		super(ManMoveXY, self).__init__(parent)
		
		# announce parent
		self.parent = parent
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# general settings
		self.setTitle('X and Y plane')
		
		# XY controls, grid layout
		sublayout_XY = QGridLayout()
		
		# initialise widgets
		self.left = QPushButton(QIcon('resources/left.svg'), '', self.parent)
		self.right = QPushButton(QIcon('resources/right.svg'), '', self.parent)
		self.up = QPushButton(QIcon('resources/up.svg'), '', self.parent)
		self.down = QPushButton(QIcon('resources/down.svg'), '', self.parent)
		
		# add widgets to vertical box layout
		sublayout_XY.addWidget(self.left, 1, 0, 1, 1)
		sublayout_XY.addWidget(self.right, 1, 2, 1, 1)
		sublayout_XY.addWidget(self.up, 0, 1, 1, 1)
		sublayout_XY.addWidget(self.down, 2, 1, 1, 1)
		
		# set sublayout as widget layout
		self.setLayout(sublayout_XY)
		
		# set geometry
		self.setFixedSize(150, 150)

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


