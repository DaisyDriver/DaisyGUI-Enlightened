from serial import Serial
from threading import Thread, Lock

class DaisyDriver(Serial):
	
	def __init__(self, connected = True):
		# check for connection bool to allow for dummy DaisyDriver object
		# if not connected
		if connected:
			# initialise DaisyDriver serial object (hard code serial address for now)
			super(DaisyDriver, self).__init__('/dev/ttyACM0')
			
			# set initial speed (0,1,2 for low,medium,high respectively)
			self.speedset(2)
			
			# initialise jog lock
			self.joglock = Lock()
			
			# initialise direction dictionary, f = forward, fl = forward left etc...
			self.directions = {'l':(0, -1, 0),
								'r':(0, 1, 0),
								'f':(-1, 0, 0),
								'fl':(-1, -1, 0),
								'fr':(-1, 1, 0),
								'b':(1, 0, 0),
								'bl':(1, -1, 0),
								'br':(1, 1, 0),
								'u':(0, 0, -1),
								'd':(0, 0, 1)}
		elif not connected:
			# just set default speedval for slider to read
			self.speedval = 2						
		
	def speedset(self, val):
		# speed val
		self.speedval = val
		
		# value from slider equals 0, 1 or 2. Use list for converting 
		# slider index to step motor speed
		speeds = [50, 275, 500]
		
		# serial command
		command = 'STV 0 {V} {V} {V} \r'.format(V=speeds[self.speedval])
		
		# convert to byte string
		bytes_command = command.encode('utf-8')
		
		# write command
		self.write(bytes_command)
		
		# flush buffer
		self.flush()
		
	def __jogdo(self, x, y, z):
		# enable lock
		with self.joglock:
						
			# flush buffer
			self.flush()
			
			# serial command
			command = 'JOG 0 {x_} {y_} {z_} \r'.format(x_=x, y_=y, z_=z)
			
			# convert to byte string
			bytes_command = command.encode('utf-8')
			
			# write command
			self.write(bytes_command)
			
			# read finish statement and print
			self.readline()
			
	def __jog(self, x, y, z, button_handle):
		# count, button status dependent
		count = 0
		
		# upper limit on jog repeats
		while count < 1000:
			if (count == 0):
				self.__jogdo(x, y, z)
		
			elif button_handle.isDown():
				self.__jogdo(x, y, z)
				
			count+=1
		
	def jog(self, direction, button_handle):
		# if not locked then jog
		if not self.joglock.locked():
			# get direction vector
			dir_tuple = self.directions[direction]
			# start jog
			jogthread = Thread(target=self.__jog, args=(*dir_tuple, button_handle))
			jogthread.start()
		

