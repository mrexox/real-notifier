"""
Abstract Daemon class
Initialization with a file where PID is stored if
a daemon was already started.

Supports `start`, `stop` and `restart`.

Must implement `run` method before usage
"""

import sys
import os
import time
import atexit
import signal
import logging
from config import Config

class Daemon:
	"""A generic daemon class.

	Usage: subclass the daemon class and override the run() method."""

	def __init__(self, pidfile): 
		self.pidfile = pidfile
		self.config = Config()
		logging.basicConfig(filename = self.config['logging']['path'] + '/notitier_daemon_log.log',
                                    filemode="w",
                                    level = self.config['logging']['level'],
                                    format = '%(asctime)s %(levelname)s: %(message)s',
                                    datefmt = '%Y-%m-%d %I:%M:%S')
		

		logging.debug("Daemon initialized.")
	        
	def _daemonize(self):
		"""Deamonize class. UNIX double fork mechanism."""

		try: 
			# копирует текущий процесс и возвращает 0,
			# если теперь находимся внутри дочернего 
			# процесса, и PID внутри родительского
			pid = os.fork() 
			if pid > 0:
				# exit first parent
				sys.exit(0) 
		except OSError as err: 
			logging.error('fork #1 failed: {0}\n'.format(err))
			sys.exit(1)
	                
		# decouple from parent environment
		os.chdir('/')
		os.setsid()
		os.umask(0) 
	        
		# do second fork
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit from second parent
				sys.exit(0) 
		except OSError as err: 
			logging.error('fork #2 failed: {0}\n'.format(err))
			sys.exit(1) 
	                
		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = open(os.devnull, 'r')
		so = open(os.devnull, 'a+')
		se = open(os.devnull, 'a+')

		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	        
		# write pidfile
		atexit.register(self._delpid)

		pid = str(os.getpid())
		with open(self.pidfile,'w+') as f:
			f.write(pid + '\n')
	                
	def _delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""Start the daemon."""

		# Check for a pidfile to see if the daemon already runs
		try:
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
		except IOError:
			pid = None
	                
		if pid:
			message = "pidfile {0} already exist. " + \
				  "Daemon already running?\n"
			logging.error(message.format(self.pidfile))
			sys.exit(1)
		        
		# Start the daemon
		self._daemonize()
		logging.debug("Daemon started")
		self._run()

	def stop(self):
		"""Stop the daemon."""

		# Get the pid from the pidfile
		try:
			with open(self.pidfile,'r') as pf:
				pid = int(pf.read().strip())
		except IOError:
			pid = None
	                
		if not pid:
			message = "pidfile {0} does not exist. " + \
				  "Daemon not running?\n"
			logging.warning(message.format(self.pidfile))
			return # not an error in a restart

		# Try killing the daemon process	
		try:
			while 1:
				os.kill(pid, signal.SIGTERM)
				time.sleep(0.1)
		except OSError as err:
			e = str(err.args)
			if e.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				logging.error(str(err.args))
				sys.exit(1)
		logging.debug("Daemon stoped")

	def restart(self):
		"""Restart the daemon."""
		self.stop()
		self.start()

	def _run(self):
		"""You should override this method when you subclass Daemon.
		
		It will be called after the process has been daemonized by 
		start() or restart()."""
		raise NotImplementedError("Should implement your own run() realization!")
