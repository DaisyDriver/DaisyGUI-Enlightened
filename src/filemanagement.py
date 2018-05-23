from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class FileDirInput(QWidget):
	
	def __init__(self, parent, camera):
		super(FileDirInput, self).__init__(parent)
		
		# announce camera
		self.camera = camera

		# init UI
		self.initUI()
		
	def initUI(self):
		# section layout
		sublayout_filedir = QHBoxLayout()
		
		# initialise widgets
		self.dirlabel = QLabel('Save Directory:')
		
		self.dirinput = QLineEdit(self.camera.savedir, self)
		self.dirinput.setFixedWidth(165)
		self.dirinput.textEdited.connect(self.ontextchange)
		
		self.dirupdate = QPushButton(QIcon('resources/done-all.svg'), 'Apply', self)
		self.dirupdate.setEnabled(False)

		# add widgets to vertical box layout
		sublayout_filedir.addWidget(self.dirlabel)
		sublayout_filedir.addWidget(self.dirinput)
		sublayout_filedir.addWidget(self.dirupdate)

		# set sublayout as widget layout
		self.setLayout(sublayout_filedir)
		
		#~ # set size
		#~ self.resize(280,40)
		
	@pyqtSlot(str)	
	def ontextchange(self, textbox_in):
		# check whether text in box different to current save directory
		# and make apply button active/inactive as appropriate
		same = (textbox_in == self.camera.savedir)
		
		if same:
			self.dirupdate.setEnabled(False)
			
		elif not same:
			self.dirupdate.setEnabled(True)

class FileManagementSection(QGroupBox):
	
	def __init__(self, parent, camera):
		super(FileManagementSection, self).__init__(parent)
		
		# announce camera handle
		self.camera = camera
		
		# init UI
		self.initUI()
		
	def initUI(self):
		# general settings
		self.setTitle('File Management')
		
		# section layout
		sublayout_fileman = QVBoxLayout()
		
		# initialise widgets
		self.dirinput = FileDirInput(self, self.camera)

		# add widgets to vertical box layout
		sublayout_fileman.addWidget(self.dirinput)

		# set sublayout as widget layout
		self.setLayout(sublayout_fileman)

	
