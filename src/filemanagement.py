from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from os.path import isdir
from pathlib import Path

class FileDirInput(QLineEdit):
	
	# signal to send to apply button
	apply_state = pyqtSignal(bool)
	
	def __init__(self, parent, camera):
		super(FileDirInput, self).__init__(camera.savedir, parent)
		
		# announce camera
		self.camera = camera

		# connect to function on change of text
		self.textChanged.connect(self.ontextchange)

	@pyqtSlot(str)	
	def ontextchange(self, textbox_in):
		# check whether text in box different to current save directory
		# and make apply button active/inactive as appropriate
		same = (textbox_in == self.camera.savedir)
		
		if same:
			self.apply_state.emit(False)
			
		elif not same:
			self.apply_state.emit(True)
			
	@pyqtSlot()
	def applydirchange(self):
		# get text from box
		textbox_mod = self.text()
		
		# ensure directory string ends and starts with '/' if not append
		if len(textbox_mod)>0 and textbox_mod[-1]!='/':
			textbox_mod = textbox_mod + '/'
			
		if len(textbox_mod)>0 and textbox_mod[0]!='/':
			textbox_mod = '/' + textbox_mod
			
		if len(textbox_mod)==0:
			textbox_mod = '/'
			
		# check directory exists, if not raise question box
		if isdir(textbox_mod):
			self.camera.savedir = textbox_mod
			
		elif not isdir(textbox_mod):
			dir_question = QMessageBox.question(self, 'Non-existent Directory', 
												'Directory: "' + textbox_mod + '" does not exist.\nDo you want to create it?', 
												QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Yes)
					
			if dir_question == QMessageBox.Yes:
				Path(textbox_mod).mkdir(parents=True, exist_ok=True)
				self.camera.savedir = textbox_mod

		# update text in box
		self.setText(textbox_mod) 
		
		# make sure apply button updates
		self.ontextchange(textbox_mod)

class SetFileFormat(QComboBox):
	
	# signal to send to apply button
	apply_state = pyqtSignal(bool)
	
	def __init__(self, parent, camera):
		super(SetFileFormat, self).__init__(parent)
		
		# announce camera handle
		self.camera = camera
		
		# initialise user interface
		self.initUI()
		
	def initUI(self):
		# add all formats
		self.addItem('jpeg')
		self.addItem('png')
		self.addItem('gif')
		self.addItem('bmp')
		self.addItem('yuv')
		self.addItem('rgb')
		self.addItem('rgba')
		self.addItem('bgr')
		self.addItem('bgra')
		
		# set to initial file format
		self.setCurrentText(self.camera.FileFormat)
		
		# connect changed to tester function for apply
		self.currentTextChanged.connect(self.ontextchange)
		
	@pyqtSlot(str)	
	def ontextchange(self, textbox_in):
		# check whether text in box different to current save directory
		# and make apply button active/inactive as appropriate
		same = (textbox_in == self.camera.FileFormat)
		
		if same:
			self.apply_state.emit(False)
			
		elif not same:
			self.apply_state.emit(True)
			
	@pyqtSlot()
	def applyformatchange(self):
		# apply file format change
		self.camera.filenameSetFormat(self.currentText())
		
class NameFormatPrefix(QLineEdit):
	
	# signal to send to apply button
	apply_state = pyqtSignal(bool)
	
	def __init__(self, parent, camera):
		super(NameFormatPrefix, self).__init__(camera.NamePrefix, parent)
		
		# announce camera
		self.camera = camera

		# connect text changed to apply button checker
		self.textChanged.connect(self.ontextchange)
		
	@pyqtSlot(str)	
	def ontextchange(self, textbox_in):
		# check whether text in box different to current save directory
		# and make apply button active/inactive as appropriate
		same = (textbox_in == self.camera.NamePrefix)
		
		if same:
			self.apply_state.emit(False)
			
		elif not same:
			self.apply_state.emit(True)
			
	@pyqtSlot()
	def applyprefixchange(self):
		# set file name format 
		self.camera.filenameSetPrefix(self.text())
		
		# update apply button
		self.ontextchange(self.text())
		
class NameFormatStamper(QWidget):
	
	def __init__(self, parent, camera):
		super(NameFormatStamper, self).__init__(parent)
		
		# announce camera
		self.camera = camera

		# init UI
		self.initUI()
		
	def initUI(self):
		# section layout
		sublayout_namestamp = QHBoxLayout()
		
		# initialise widgets
		self.checkboxdate = QCheckBox('Date', self)
		self.checkboxtime = QCheckBox('Time', self)

		# add widgets to vertical box layout
		sublayout_namestamp.addWidget(self.checkboxdate)
		sublayout_namestamp.addWidget(self.checkboxtime)

		# set sublayout as widget layout
		self.setLayout(sublayout_namestamp)
		
		# reduce automatic height
		self.setFixedHeight(35)
		
	#~ @pyqtSlot(str)	
	#~ def ontextchange(self, textbox_in):
		#~ # check whether text in box different to current save directory
		#~ # and make apply button active/inactive as appropriate
		#~ same = (textbox_in == self.camera.NamePrefix)
		
		#~ if same:
			#~ self.nameupdate.setEnabled(False)
			
		#~ elif not same:
			#~ self.nameupdate.setEnabled(True)
			
	#~ @pyqtSlot()
	#~ def applytextchange(self):
		#~ # set file name format 
		#~ self.camera.filenameSetPrefix(self.nameinput.text())
		
		#~ # update apply button
		#~ self.ontextchange(self.nameinput.text())
		
		
class ApplyButton(QPushButton):
	
	def __init__(self, parent, camera):
		super(ApplyButton, self).__init__(QIcon('resources/done-all.svg'), 'Apply', parent)
		
		# announce camera handle
		self.camera = camera
		
		# set inactive initially as boxes all contain defaults
		self.setEnabled(False)
		
class AdvancedSettingsButton(QPushButton):
	
	def __init__(self, parent, camera):
		super(AdvancedSettingsButton, self).__init__(QIcon('resources/cog.svg'), 'Settings', parent)
		
		# announce camera handle
		self.camera = camera
		
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
		sublayout_fileman = QFormLayout()
		
		# initialise widgets
		self.dirinput = FileDirInput(self, self.camera)
		self.fileformat = SetFileFormat(self, self.camera)
		self.nameformat = NameFormatPrefix(self, self.camera)
		self.namestamper = NameFormatStamper(self, self.camera)
		self.applybutton = ApplyButton(self, self.camera)
		self.adsetbutton = AdvancedSettingsButton(self, self.camera)

		# add widgets to vertical box layout
		sublayout_fileman.addRow(QLabel('Save Directory:'), self.dirinput)
		sublayout_fileman.addRow(QLabel('File Format:'), self.fileformat)
		sublayout_fileman.addRow(QLabel('File Name Prefix:'), self.nameformat)
		sublayout_fileman.addRow(QLabel('Include Stamps:'), self.namestamper)
		sublayout_fileman.addRow(self.adsetbutton, self.applybutton)

		# set sublayout as widget layout
		self.setLayout(sublayout_fileman)
		
		# set geometry
		#~ self.setFixedSize(sublayout_fileman.sizeHint())
		
		# make connections between slots and signals
		self.makeconnections()
		
	def makeconnections(self):
		
		# from directory text box to apply button
		self.dirinput.apply_state.connect(self.applybutton.setEnabled)
		# from apply button to directory text box
		self.applybutton.clicked.connect(self.dirinput.applydirchange)

		# from file format combo box to apply button
		self.fileformat.apply_state.connect(self.applybutton.setEnabled)
		# from apply button to format combox box
		self.applybutton.clicked.connect(self.fileformat.applyformatchange)
		
		# from name prefix text box to apply button
		self.nameformat.apply_state.connect(self.applybutton.setEnabled)
		# from apply button to directory text box
		self.applybutton.clicked.connect(self.nameformat.applyprefixchange)
		


	
