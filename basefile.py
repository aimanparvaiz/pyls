
from __future__ import division
import os
import stat
import sys
import pwd
import grp
import time
import glob

def get_links_to_inode(l_file):
		return os.stat(l_file).st_nlink
	

def get_last_modification_time(l_file):
	t_sec = os.stat(l_file).st_mtime
	# Change time in s since epoch to struct_time

	# Change struct_time to string given by format arg
	return time.strftime("%b %d %H:%M", time.gmtime(t_sec))

def get_mode(l_file):
	perms="-"
	link=""
	#mode = int(oct(stat.S_IMODE(os.stat(l_file).st_mode)))
	mode = os.stat(l_file).st_mode
	
	if stat.S_ISLNK(mode):
		perms = "l"
		link = os.readlink(l_file)
		#f not os.path.exists(l_file):
	elif stat.S_ISDIR(mode):
		perms = "d"
	for who in "USR", "GRP", "OTH" :
		for what in "R", "W", "X":
			if mode & getattr(stat, "S_I"+what+who):
				perms=perms+what.lower()
			else:
				perms=perms+"-"
	return (perms, link)		

def get_file_owners(l_file):
	uid = os.stat(l_file).st_uid
	gid = os.stat(l_file).st_gid
	
	user = pwd.getpwuid(uid)[0]
	group = grp.getgrgid(gid)[0]
	
	return (user, group)

def get_file_size(l_file):
	size = os.stat(l_file).st_size
	return size


def temp(dir_obj, file_obj, flags):
	ls_output = []
	all_content = [dir_obj] + [file_obj]
	if 'a' in flags:
        for all_object in all_content:
            ls_output += all_object.fname
    if 'l' in flags:
        if len(ls_output) == 0:
            #Just ls -l
            for content in all_content:
                ls_output += content.option_l(content.fname)
    print ls_output


def identify_type(cwd, flags):
    file_obj = []
    dir_obj = []

    dir_contents = os.listdir(cwd)

    for dir_content in dir_contents:
        mode = os.stat(dir_content).st_mode

        if stat.S_ISLNK(mode):
          Symlink(cwd, flags, dir_content)
        elif stat.S_ISDIR(mode):
          dir_obj.append(Dir(cwd, flags, dir_content))
        else:
          file_obj.append(File(cwd, flags, dir_content))

    temp(dir_obj, file_obj)


class Basefile(object):
	"""
	All the funcions which can be executed on a file should go here

	"""

	def __init__(self, cwd, flags, dir_content):
		self.cwd = cwd
		self.flags = flags
		self.fname = dir_content
		self.ls_output = []

	
	def output(self):
	 	pass


	def option_l(self, fname):
		result = []
		total_size = 0
		perms, link = get_mode(fname)
		user, grp = get_file_owners(fname)
		size = get_file_size(fname)
		total_size = total_size+size
		links = get_links_to_inode(fname)
		mtime = get_last_modification_time(fname)
		result = [perms, links, user, grp, size, mtime, fname]
		return result

class Dir(Basefile):
	def __init__(self, cwd, flags, dir_content):
		Basefile.__init__(self, cwd, flags, dir_content)

class File(Basefile):
	def __init__(self, cwd, flags, dir_content):
		self.cwd = cwd
		self.flags = flags
		self.fname = dir_content
		Basefile.__init__(self, cwd, flags, dir_content)

	def output(self):
		ls_output = []
		hidden = False
		#AHC = False

		# Check for hidden
		if self.fname[0] == '.':
			hidden = True

		if 'a' in self.flags:
			ls_files = [os.curdir, os.pardir, self.fname] 
			ls_output = ls_files
		
		if 'A' in self.flags:
			ls_files = [self.fname]
			# long list
			ls_output = ls_files

		if 't' in self.flags:
			# sort on the mtime
			pass

		if 'l' in self.flags:
			# long list
			if len(ls_output) == 0:
				# Plain ls -l, wont show hidden files
				if hidden:
					return
				else:
					ls_files = [ self.fname ] 

			else:
				ls_files = ls_output 

			for ls_file in ls_files:
				#import ipdb; ipdb.set_trace()
				# Why isnt . and .. not showing up in ls -la
				ls_output = self.option_l(ls_file)
		
		print ls_output	




class Symlink(Basefile):
	def __init__(self, cwd, flags, dir_content):
		Basefile.__init__(self, cwd, flags, dir_content)

if __name__ == '__main__':
	
	identify_type(sys.argv[1], sys.argv[2:])

				
