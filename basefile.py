
from __future__ import division
from ls_file_attributes import *
import os
import stat

def identify_type(cwd, flags):
	# find all files in the listed directory 
	dir_contents = os.listdir(cwd)

	# find type; dir, file, symlink
	for dir_content in dir_contents:
		mode = os.stat(dir_content).st_mode

		if stat.S_ISLINK(mode):
			Symlink(cwd, flags).output()

		elif stat.S_ISDIR(mode):
			Dir(cwd, flags).output()

		else:
			# Good old plain file :)
			File(cwd, flags).output()



class Basefile(object):
	"""
	All the funcions which can be executed on a file should go here

	"""

	def __init__(self, cwd, flags):
		self.cwd = cwd
		self.flags = flags
		ls_output = []

	
	def output(self):

		if 'a' in flags:
			# Got all hidden files in list
			ls_output+= [os.curdir, os.pardir] + os.listdir(self.cwd)	
		
		if 'l' in flags:
			# ls_output is accessible here too
			# l|long list format is the last one to be parsed.
			if ls_output.len() == 0:
				# Just ls -l
				ls_output+=option_l(self.cwd)
			else:
				# ls_output is the list we need to work on
				ls_output+=option_l(self.cwd, ls_output)
		print ls_output



	# Option -l
	def option_l(cwd, ls_output=None):
		result = []
		total_size = 0
		if ls_output is None:
			ls_output = os.listdir(cwd)
			ls_files = [ files for files in ls_output if files[0] != '.' ]
		else:
			l_files = ls_output 

		for l_file in ls_files:
			perms, link = self.get_mode(l_file)
			user, grp = self.get_file_owners(l_file)
			size = self.get_file_size(l_file)
			total_size = total_size+size
			links = self.get_links_to_inode(l_file)
			mtime = self.get_last_modification_time(l_file)
			result = [perms, links, user, grp, size, mtime, l_file]
			return result

class Dir(Basefile):
	def __init__(self, cwd, flags):
		Basefile.__init__(self, cwd, flags)

class File(Basefile):
	def __init__(self, cwd, flags):
		Basefile.__init__(self, cwd, flags)

class Symlink(Basefile):
	def __init__(self, cwd, flags):
		Basefile.__init__(self, cwd, flags)

if __name__ == '__main__':
	identify_type(sys.argv[1], sys.argv[2:])

				
