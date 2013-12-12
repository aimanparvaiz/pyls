
import os

class Basefile(object):
	"""
	All the funcions which can be executed on a file should go here

	"""

	def __init__(self):
		print 'dont know what to initialize :)'

	# Option -a
	def a(self, dir_path=None):
		# If dir_path in None then show all files in current dir
		if not dir_path:
			dir_path = os.getcwd()
		# Everything in the present dir is in files now	
		a_files = os.listdir(dir_path)
		return a_files

	# Option -l
	def l(self, dir_path=None):
		if not dir_path:
			dir_path = os.getcwd()
		l_files = os.listdir(dir_path)
		l_files = [ files for files in l_files if files[0] != '.' ]
		return l_files

class just_file(Basefile):

	def stdout(self):
		a_files = self.a()
		#l_files = self.l()
		for a_file in a_files:
			print a_file
			
if __name__ == '__main__':
	obj1 = just_file()
	obj1.stdout()
