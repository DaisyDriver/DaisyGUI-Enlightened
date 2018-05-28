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
		
		# set geometry
		self.setFixedHeight(55)
		
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
		validchars = '0123456789'
		
		if not all([char in validchars for char in textnumber]):
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
			
	@pyqtSlot()
	def applyqualchange(self):
		# set fset to value
		self.fset.JPGquality = self.qualslide.value()
		
		# update apply button
		self.onslidechange(self.qualslide.value())
			
class CustomFileName(QWidget):
	
	# signal to send to apply button
	apply_state = pyqtSignal(bool, str)
	# signal to enable/disable non custom file name settings
	custom_state = pyqtSignal(bool)
	
	def __init__(self, parent, fset):
		super(CustomFileName, self).__init__(parent)
		
		# announce fset
		self.fset = fset
		
		# init ui
		self.initUI()
		
		# connect check boxes
		self.customswitch.stateChanged.connect(self.customstateswitch)
		self.customswitch.stateChanged.connect(self.customapplyswitch)
		
		# connect text box
		self.customname.textEdited.connect(self.customapplyname)
		
	def initUI(self):
		
		# set layout
		cfn_layout = QHBoxLayout()
		
		# add widgets
		self.customswitch = QCheckBox(self)
		self.customname = QLineEdit(self.fset.customname, self)
		
		# set custom state as appropriate
		self.customswitch.setCheckState(int(self.fset.custombool))
		self.customswitch.setTristate(False)
		self.customname.setEnabled(self.fset.custombool)
		
		# add widgets to layout
		cfn_layout.addWidget(self.customswitch)
		cfn_layout.addWidget(self.customname)
		
		# set layout to widget
		self.setLayout(cfn_layout)
		
		# adjust geometries
		self.customname.setFixedWidth(400)
		self.setFixedHeight(55)
		
	@pyqtSlot(int)	
	def customapplyswitch(self, customswitch_in):
		# check whether custombool matches check box
		# and make apply button active/inactive as appropriate
		same = (bool(customswitch_in) == self.fset.custombool)
		
		if same:
			self.apply_state.emit(False, 'CustomFileSwitch')
			
		elif not same:
			self.apply_state.emit(True, 'CustomFileSwitch')
			
	@pyqtSlot(int)	
	def customstateswitch(self, customswitch_in):
		# get custom as bool
		val = bool(customswitch_in)
		
		# set custom text box state
		self.customname.setEnabled(val)
			
	@pyqtSlot(str)	
	def customapplyname(self, customname_in):
		# check whether customname matches line edit box
		# and make apply button active/inactive as appropriate
		same = (customname_in == self.fset.customname)
		
		if same:
			self.apply_state.emit(False, 'CustomFileName')
			
		elif not same:
			self.apply_state.emit(True, 'CustomFileName')

	@pyqtSlot()
	def applycustomchange(self):
		# set custom file name to line edit contents
		self.fset.customname = self.customname.text()
		
		# set custom bool
		self.fset.custombool = self.customswitch.isChecked()
		
		# update name using helper function
		self.fset.filenameswitcher()
		
		# update apply button
		self.apply_state.emit(False, 'CustomFileName')
		self.apply_state.emit(False, 'CustomFileSwitch')
		
		# emit state to non custom boxes
		self.custom_state.emit(not self.customswitch.isChecked())
			
class ApplyButton(QPushButton):
	
	def __init__(self, parent, fset):
		super(ApplyButton, self).__init__(QIcon('resources/done-all.svg'), 'Apply', parent)
		
		# announce fset handle
		self.fset = fset
		
		# set inactive initially as boxes all contain current values
		self.setEnabled(False)
		
		# dictionary keeping track of all changed
		self.changedict = {'RawCheck':False, 'QualJPEG':False, 'CustomFileSwitch':False, 'CustomFileName':False}
	
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
			
class CancelButton(QPushButton):
	
	def __init__(self, parent):
		super(CancelButton, self).__init__('Close', parent)
		
		# announce parent
		self.parent = parent
		
		# connect click to close parent
		self.clicked.connect(self.closedialog)
		
	@pyqtSlot()
	def closedialog(self):
		# close parent window (advanced settings)
		self.parent.close()		

class AdvancedSettingsWindow(QDialog):
	
	def __init__(self, parent, fset):
		super(AdvancedSettingsWindow, self).__init__(parent)
		
		# announce parent
		self.parent = parent
		
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
		self.custname = CustomFileName(self, self.fset)
		self.applybutton = ApplyButton(self, self.fset)
		
		# add widgets to layout
		fileset_layout.addRow(QLabel('Include raw Bayer data? (JPEG only)'), self.rawcheck)
		fileset_layout.addRow(QLabel('Quality of compression (JPEG only)'), self.qualjpeg)
		fileset_layout.addRow(QLabel('Use custom file name?'), self.custname)
		fileset_layout.addRow(CancelButton(self), self.applybutton)
		
		# set spacing
		fileset_layout.setSpacing(1)
		
		# set settings_layout as widget layout
		self.setLayout(fileset_layout)
		
		# set window geometry
		self.setFixedSize(fileset_layout.sizeHint())
		
	def makeconnections(self):
		
		# from raw check box to apply button
		self.rawcheck.apply_state.connect(self.applybutton.individualSetEnable)
		# from apply button to raw check box
		self.applybutton.clicked.connect(self.rawcheck.applyrawchange)
		
		# from jpeg quality slider to apply button
		self.qualjpeg.apply_state.connect(self.applybutton.individualSetEnable)
		# from apply button to slider set
		self.applybutton.clicked.connect(self.qualjpeg.applyqualchange)
		
		# from custom state to apply
		self.custname.apply_state.connect(self.applybutton.individualSetEnable)
		# from advanced settings to normal settings
		self.custname.custom_state.connect(self.parent.nameformat.setEnabled)
		self.custname.custom_state.connect(self.parent.namestamper.setEnabled)
		# from apply button to custom state apply
		self.applybutton.clicked.connect(self.custname.applycustomchange)
