from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from os.path import isdir
from pathlib import Path

class RawCheck(QCheckBox):
	
	# signal to send to apply button
	apply_state = pyqtSignal(bool, str)
	
	def __init__(self, parent, fset):
		super(RawCheck, self).__init__('', parent)
		
		# announce fset
		self.fset = fset

		# set check state as appropriate
		self.setCheckState(int(self.fset.bayerInclude))
		self.setTristate(False)
		
		# connect check box
		self.stateChanged.connect(self.onrawchange)
		
		# reduce height
		self.setFixedHeight(25)
		
	@pyqtSlot(int)	
	def onrawchange(self, rawbox_in):
		# check whether raw bool matches check box
		# and make apply button active/inactive as appropriate
		same = (bool(rawbox_in) == self.fset.bayerInclude)
		
		if same:
			self.apply_state.emit(False, 'RawCheck')
			
		elif not same:
			self.apply_state.emit(True, 'RawCheck')
			
	@pyqtSlot()
	def applyrawchange(self):
		# set raw bool
		self.fset.bayerInclude = self.isChecked()
		
		# test and update apply button
		self.onrawchange(int(self.isChecked()))
		
class QualJPEG(QWidget):

	# signal to send to apply button
	apply_state = pyqtSignal(bool, str)
	
	def __init__(self, parent, fset):
		super(QualJPEG, self).__init__(parent)
		
		# announce fset handle
		self.fset = fset
		
		# init UI
		self.initUI()
		
		# connect signals and slots
		self.makeconnections()
		
	def initUI(self):
		
		# QualJPEG layout
		qual_layout = QGridLayout()
		
		# init widgets
		self.qualslide = QSlider(Qt.Horizontal, self)
		self.qualnum = QLineEdit(self)
		
		# customise widgets
		self.qualslide.setMinimum(1)
		self.qualslide.setMaximum(100)
		self.qualslide.setFixedHeight(20)
		self.qualslide.setValue(self.fset.JPGquality)
		
		self.qualnum.setFixedWidth(35)
		self.qualnum.setText(str(self.fset.JPGquality))
		
		# add widgets to layout
		qual_layout.addWidget(self.qualslide, 0, 0, 3, 1)
		qual_layout.addWidget(self.qualnum, 0, 4, 1, 1)
		
		# set layout to widget
		self.setLayout(qual_layout)
		
	def makeconnections(self):
		# connect slide change to text box
		self.qualslide.valueChanged.connect(self.updateboxnumber)
		# connect text box to format checker and slide change
		self.qualnum.returnPressed.connect(self.updateslideposition)
		
		# connect slide change to apply button test
		self.qualslide.valueChanged.connect(self.onslidechange)
		
	@pyqtSlot(int)
	def updateboxnumber(self, slider_in):
		self.qualnum.setText(str(slider_in))
		
	@pyqtSlot()
	def updateslideposition(self):
		
		# get text
		textnumber = self.qualnum.text()
		
		# check for validity
		validnums = '0123456789'
		
		if not all([char in validnums for char in textnumber]):
			error_dialog = QMessageBox.critical(self, 'Incorrect number input', 
												'Input number must be an integer between 1 and 100 inclusive',
												QMessageBox.Ok)
			return 

		number_in = int(textnumber)
		
		if number_in<1:
			error_dialog = QMessageBox.critical(self, 'Incorrect number input', 
												'Input number must be an integer between 1 and 100 inclusive',
												QMessageBox.Ok)
			return 
		
		elif number_in>100:
			error_dialog = QMessageBox.critical(self, 'Incorrect number input', 
									'Input number must be an integer between 1 and 100 inclusive',
									QMessageBox.Ok)
			return 
			
		# passed tests so update slider
		self.qualslide.setValue(int(number_in))
		
	@pyqtSlot(int)
	def onslidechange(self, slider_in):
		# check whether raw bool matches check box
		# and make apply button active/inactive as appropriate
		same = (slider_in == self.fset.JPGquality)
		
		if same:
			self.apply_state.emit(False, 'QualJPEG')
			
		elif not same:
			self.apply_state.emit(True, 'QualJPEG')
				
class ApplyButton(QPushButton):
	
	def __init__(self, parent, fset):
		super(ApplyButton, self).__init__(QIcon('resources/done-all.svg'), 'Apply and Close Window', parent)
		
		# announce fset handle
		self.fset = fset
		
		# set inactive initially as boxes all contain current values
		self.setEnabled(False)
		
		# dictionary keeping track of all changed
		self.changedict = {'RawCheck':False, 'QualJPEG':False, 'CustomFileName':False}
	
	@pyqtSlot(bool, str)
	def individualSetEnable(self, inbool, inkey):
		self.changedict[inkey] = inbool
		
		# run check
		self.checkallstates()
	
	def checkallstates(self):
		# check everything False, if so disable apply
		if all(value == False for value in self.changedict.values()):
			self.setEnabled(False)
		
		elif any(value == True for value in self.changedict.values()):
			self.setEnabled(True)

class AdvancedSettingsWindow(QDialog):
	
	def __init__(self, parent, fset):
		super(AdvancedSettingsWindow, self).__init__(parent)
		
		# announce fset variable
		self.fset = fset
		
		# initialise user interface
		self.initUI()

		# make connections between slots and signals
		self.makeconnections()
		
	def initUI(self):
		# set title
		self.setWindowTitle('Advanced File Settings')
		
		# set layout
		fileset_layout = QFormLayout()
		
		# get widgets
		self.rawcheck = RawCheck(self, self.fset)
		self.qualjpeg = QualJPEG(self, self.fset)
		
		self.applybutton = ApplyButton(self, self.fset)
		
		# add widgets to layout
		fileset_layout.addRow(QLabel('Include raw Bayer data? (JPEG only)'), self.rawcheck)
		fileset_layout.addRow(QLabel('Quality of compression (JPEG only)'), self.qualjpeg)
		
		
		fileset_layout.addRow(QLabel('cancel placeholder'), self.applybutton)
		
		# set settings_layout as widget layout
		self.setLayout(fileset_layout)
		
		# set window geometry
		#~ self.setFixedSize(fileset_layout.sizeHint())
		
	def makeconnections(self):
		
		# from raw check box to apply button
		self.rawcheck.apply_state.connect(self.applybutton.individualSetEnable)
		# from apply button to raw check box
		self.applybutton.clicked.connect(self.rawcheck.applyrawchange)
		
		# from jpeg quality slider to apply button
		self.qualjpeg.apply_state.connect(self.applybutton.individualSetEnable)
		# from apply button to slider set
		#~ self.applybutton.clicked.connect(self.rawcheck.applyqualchange)

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
