from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class CameraTimerSection(QGroupBox):
	
	def __init__(self, parent, camera):
		super(CameraTimerSection, self).__init__(parent)
		
		# announce camera handle
		self.camera = camera
		
		# init UI
		self.initUI()

		# make connections between slots and signals
		#~ self.makeconnections()
		
	def initUI(self):
		# general settings
		self.setTitle('Camera Timer')
		
		# section layout
		sublayout_fileman = QFormLayout()
		
		# initialise widgets

		# add widgets to vertical box layout

		# set sublayout as widget layout
		self.setLayout(sublayout_fileman)
		
		# set geometry
		#~ self.setFixedSize(sublayout_fileman.sizeHint())
		
	#~ def makeconnections(self):
		
		#~ # from directory text box to apply button
		#~ self.dirinput.apply_state.connect(self.applybutton.individualSetEnable)
		#~ # from apply button to directory text box
		#~ self.applybutton.clicked.connect(self.dirinput.applydirchange)

		#~ # from file format combo box to apply button
		#~ self.fileformat.apply_state.connect(self.applybutton.individualSetEnable)
		#~ # from apply button to format combox box
		#~ self.applybutton.clicked.connect(self.fileformat.applyformatchange)
		
		#~ # from name prefix text box to apply button
		#~ self.nameformat.apply_state.connect(self.applybutton.individualSetEnable)
		#~ # from apply button to directory text box
		#~ self.applybutton.clicked.connect(self.nameformat.applyprefixchange)
		
		#~ # from date/time stamp check boxes to apply button
		#~ self.namestamper.apply_state.connect(self.applybutton.individualSetEnable)
		#~ # from apply button to date/time stamp box confirmation
		#~ self.applybutton.clicked.connect(self.namestamper.applystampchange)

