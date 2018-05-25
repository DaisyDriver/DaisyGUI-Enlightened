import serial

class DaisyDriver():
	
	def __init__(self):
		# initialise DaisyDriver serial object (hard code serial address for now)
		self.DD = serial.Serial('/dev/ttyACM0')
		
	def __jog(self, x, y, z):
		# serial command
		command = 'JOG 0 {x_} {y_} {z_} \r'.format(x_=x, y_=y, z_=z)
		
		# convert to byte string
		bytes_command = command.encode('utf-8')
		
		# write command
		self.DD.write(bytes_command)
		
	def jogLeft(self):
		self.__jog(1, 0, 0)
		
	def jogRight(self):
		self.__jog(-1, 0, 0)
		
	def jogUpY(self):
		self.__jog(0, 1, 0)
		
	def jogUpLeft(self):
		self.__jog(1, 1, 0)
		
	def jogUpRight(self):
		self.__jog(-1, 1, 0)
		
	def jogDownY(self):
		self.__jog(0, -1, 0)

	def jogDownLeft(self):
		self.__jog(1, -1, 0)
		
	def jogDownRight(self):
		self.__jog(-1, -1, 0)
		
	def jogUpZ(self):
		self.__jog(0, 0, 1)
		
	def jogDownZ(self):
		self.__jog(0, 0, -1)
		

