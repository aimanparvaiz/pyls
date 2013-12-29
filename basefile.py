
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


def ls_output_generator(dir_obj, file_obj, flags):
	# temp has all content view
	ls_output = []
	all_content = dir_obj + file_obj
	if 'a' in flags:
		ls_output += [os.curdir, os.pardir]
		for all_object in all_content:
			ls_output.append(all_object.fname)	
			
	if 'd' in flags:
		print "This is d option"
		for all_dir_obj in dir_obj:
			ls_output.append(all_dir_obj.fname)
		ls_output.append(os.curdir)	

	if 'A' in flags:
		print "This is A option"
		for all_object in all_content:
			ls_output.append(all_object.fname)

	if 't' in flags:
		print "This is t option"
		mtime_list=[]
		for content in all_content:
			mtime_list += [get_last_modification_time(content.fname)]
		ls_output += list(sorted(mtime_list))



	if 'l' in flags:
		if len(ls_output) == 0:
		#Just ls -l
			print "this is simple -l option"
			for content in all_content:
				if content.fname[0] != '.':
					ls_output += content.option_l(content.fname)
		else:
			print "This is not so simple option"
			temp_out = [b for a in ls_output for b in all_content if a == b.fname]
			all_content = list(temp_out) # Got relevant objects
			ls_output = []
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
        	d_obj = Dir(cwd, flags, dir_content)
          	dir_obj.append(d_obj)
        else:
        	f_obj = File(cwd, flags, dir_content)
          	file_obj.append(f_obj) # All files list
    ls_output_generator(dir_obj, file_obj, flags)


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


class Symlink(Basefile):
	def __init__(self, cwd, flags, dir_content):
		Basefile.__init__(self, cwd, flags, dir_content)

if __name__ == '__main__':
	
	identify_type(sys.argv[1], sys.argv[2:])

				
