############################################################
# Module  : Trace program execution and print to screen
# Date    : March 23rd, 2017
# Author  : Xiao Ling
############################################################

import os
import datetime

############################################################
'''
	Class
'''
class Writer:
	'''
		@Use: construct writer instance to print to screen
		      and write output to `log_dir`
		      with tabs `tabs` preceding each line
		      if function is in `debug` mode. 
		      print `debug mode on screen`

		@Returns: a `Writer` instance

		@Methods:

			tell  :: String -> IO ()
				prints message to screen and write 
				message to output file

				Throws: ValueError: if Handle is closed

			close :: IO ()
				closes IO Handle

	'''
	def __init__(self, log_dir, tabs=0, debug = False):
		if not os.path.exists(log_dir):
			raise NameError("\n\t>> no directory at " + log_dir)
		else:
			name   = 'log-' + '-'.join(str(datetime.datetime.now()).split(' ')) + '.txt'
			self.h = open(os.path.join(log_dir, name), 'w')
			self.tabs = '\t'*tabs + '>> '
			if debug:
				mode = ' in DEBUG mode '
			else:
				mode = ' in PRODUCTION mode '

			self.tell('='*10 + mode + '='*10)

	def tell(self,msg):
		print('\n' + self.tabs + msg)
		self.h.write('\n' + self.tabs + msg)

	def close(self):
		self.h.write('\n' + self.tabs + 'END')
		self.h.close()














