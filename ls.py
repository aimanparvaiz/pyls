from __future__ import division
import file_attribute_getter 
import os
import stat
import sys
import pwd
import grp
import time
import glob


def ls_output_generator(dir_obj, file_obj, flags):
	all_obj = dir_obj + file_obj
	output_str = ''
	for obj in all_obj:
		if 'i' in flags:
			output_str += str(obj.get_inode_number(obj.fname)) + ' '
		if 'm' in flags:
			output_str += obj.fname+','+' '
	print output_str
		




def identify_type(cwd, flags):
	file_obj = []
	dir_obj = []

	dir_contents = os.listdir(cwd)

	for dir_content in dir_contents:
		mode = os.stat(dir_content).st_mode

		if stat.S_ISLNK(mode):
		  Symlink(cwd, flags, dir_content)

		elif stat.S_ISDIR(mode):
			d_obj = Dir(cwd, flags, dir_content)
			dir_obj.append(d_obj)
			if 'a' in flags:
				dir_obj = [Dir(cwd, flags, '..')] + dir_obj
				dir_obj = [Dir(cwd, flags, '.')] + dir_obj
		else:
			f_obj = File(cwd, flags, dir_content)
			file_obj.append(f_obj) # All files list

	ls_output_generator(dir_obj, file_obj, flags)

class Basefile(object):
	def __init__(self, cwd, flags, dir_content):
		self.cwd = cwd
		self.flags = flags
		self.fname = dir_content
		self.ls_output = []

	def get_inode_number(self, fname):
		return os.stat(fname).st_ino


class Dir(Basefile):
	def __init__(self, cwd, flags, dir_content):
		Basefile.__init__(self, cwd, flags, dir_content)


class File(Basefile):
	def __init__(self, cwd, flags, dir_content):
		Basefile.__init__(self, cwd, flags, dir_content)


class Symlink(Basefile):
	def __init__(self, cwd, flags, dir_content):
		Basefile.__init__(self, cwd, flags, dir_content)

if __name__ == '__main__':
	
	identify_type(sys.argv[1], sys.argv[2:])