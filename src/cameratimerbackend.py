from threading import Timer, Thread
from time import time

class RepeatedTimer():
	def __init__(self, interval, function, timelimit = None, countlimit = None, callback = None):
		# announce interval to class
		self.interval = interval
		
		# announce target function to class
		self.function = function
		
		# init variable for 
		self.is_running = False
		
		# error catching
		assert not ((timelimit is not None) and (countlimit is not None)), 'Cannot use both time limit and count limit'
			
		assert not ((timelimit is None) and (countlimit is None)), 'Time limit xor count limit must be defined'
		
		# announce countlimit
		self.countlimit = countlimit
		
		if timelimit is not None:
			# announce timelimit
			self.timelimit = timelimit
		elif self.countlimit is not None:
			# convert countlimit to timelimit 
			self.timelimit = self.interval*countlimit - self.interval/2
			
		# recalibrate time limit to take into account first run at time t=0
		self.timelimit = self.timelimit - self.interval
			
		# announce callback function
		self.callback = callback	
			
	def __run(self):
	  
		self.is_running = False
		
		self.start_it()
		
		self.function()
	
	def start_it(self):
		
		if not self.is_running and (time() - self.time_init) < self.timelimit:
			
			self.next_call += self.interval
			
			self._timer = Timer(self.next_call - time(), self.__run)
			
			self._timer.start()
			
			self.is_running = True
			
		else:
			
			self.stop()
			
	def start_all(self):
	
		# get starting time for time limit
		self.time_init = time()
		
		# start 0th instance
		initial_thread = Thread(target=self.function)
		initial_thread.start()
	
		# get starting time for 0th timed call
		self.next_call = time()
		
		self.start_it()
			
	def stop(self):
	  
		self._timer.cancel()
		
		self.is_running = False
		
		if self.callback is not None:
			self.callback()
