########################################################################

#~ from threading import Timer, Lock, Thread
#~ from time import sleep

#~ def doslowthing():
	#~ print('starting slow thing')
	#~ sleep(5)
	#~ print('finishing slow thing')
	
#~ t1 = Timer(0.0, doslowthing)
#~ t2 = Timer(2.5, doslowthing)

#~ t1.start()
#~ t2.start()

########################################################################

#~ import schedule
#~ from datetime import datetime
#~ from time import sleep, time
#~ import threading

#~ def doslowthing():
	#~ print('starting slow thing at', 'time {timestamp:%H:%M:%S...%f}'.format(timestamp=datetime.now()))
	#~ sleep(5)
	
#~ def STthreaded():
	#~ th = threading.Thread(target=doslowthing)
	#~ th.start()
	
#~ schedule.every().second.do(STthreaded)

#~ t0 = time()
#~ while 1:
    #~ schedule.run_pending()

########################################################################

#~ from threading import Thread, Timer
#~ from time import sleep
#~ from datetime import datetime

#~ def waitawhile(i,t):
	#~ print('thread',i,'starting')
	#~ sleep(t)
	#~ print('thread',i,'stopping')
	
#~ t1 = Thread(target=waitawhile, args = (1,100), daemon=True)
#~ t2 = Thread(target=waitawhile, args = (2,3), daemon=False)

#~ t1.start()
#~ t2.start()

########################################################################

#~ from threading import Thread, Timer
#~ from time import sleep
#~ from datetime import datetime

#~ def waitawhile(i,t):
	#~ print('thread',i,'starting')
	#~ sleep(t)
	#~ print('thread',i,'stopping')
	
#~ t1 = Thread(target=waitawhile, args = (1,100), daemon=True)
#~ t2 = Thread(target=waitawhile, args = (2,3), daemon=False)

#~ t1.start()
#~ t2.start()

########################################################################

from threading import Timer, Thread
import time
from datetime import datetime

def doslowthing():
	print('starting slow thing at', 'time {timestamp:%H:%M:%S...%f}'.format(timestamp=datetime.now()))
	time.sleep(5)

class RepeatedTimer():
	def __init__(self, interval, function, timelimit=None, countlimit=None):
	  
		self._timer = None
		
		self.interval = interval
		
		self.function = function
		
		self.is_running = False
		
		# error catching
		assert not ((timelimit is not None) and (countlimit is not None)), 'Cannot use both time limit and count limit'
			
		assert not ((timelimit is None) and (countlimit is None)), 'Time limit xor count limit must be defined'
		
		if timelimit is not None:
			# announce timelimit
			self.timelimit = timelimit
		elif countlimit is not None:
			# convert countlimit to timelimit 
			self.timelimit = self.interval*countlimit #+ self.interval/2
			
		# recalibrate time limit to take into account first run at time t=0
		self.timelimit = self.timelimit - self.interval
			
	def __run(self):
	  
		self.is_running = False
		
		self.start_it()
		
		self.function()
	
	def start_it(self):
		
		if not self.is_running and (time.time() - self.time_init) < self.timelimit:
			
			self.next_call += self.interval
			
			self._timer = Timer(self.next_call - time.time(), self.__run)
			
			self._timer.start()
			
			self.is_running = True
			
		else:
			
			self.stop()
			
	def start(self):
		
			self.time_init = time.time()
			
			initial_thread = Thread(target=self.function)
			initial_thread.start()
		
			self.next_call = time.time()
			
			self.start_it()
			
	def stop(self):
	  
		self._timer.cancel()
		
		self.is_running = False

# count limit version
#~ a = RepeatedTimer(1, doslowthing, countlimit=7)
#~ print('START-----------------', 'time {timestamp:%H:%M:%S...%f}'.format(timestamp=datetime.now()))
#~ a.start()
# works ok

# time limit version
#~ a = RepeatedTimer(3, doslowthing, timelimit = 10)
#~ print('START-----------------', 'time {timestamp:%H:%M:%S...%f}'.format(timestamp=datetime.now()))
#~ a.start()
# works ok

########################################################################



