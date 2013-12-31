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
		if 'l' in flags:
			output_str += obj.long_list_format(obj.fname)
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

	def long_list_format(self, fname):
		result = ''
		total_size = 0
		perms, link = self.get_mode(fname)
		user, grp = self.get_file_owners(fname)
		size = self.get_file_size(fname)
		total_size = total_size+size
		links = self.get_links_to_inode(fname)
		mtime = str(self.get_last_modification_time(fname))
		result += ' '+perms+' '+str(links)+' '+user+' '+grp+' '+str(size)+' '+str(mtime)+' '+fname
		return result

	def assert_non_hidden(self, fname):
		if fname[0] != '.':
			return True

	def human_readable_file_size(self, num):
		for x in ['B','K','M','G','T']:
			if num < 1024.0:
				if x == 'B':
					return num
				else:
					return "%3.1f%s" % (num, x)
			num = num/1024.0

	def get_links_to_inode(self, fname):
			return os.stat(fname).st_nlink
		

	def get_last_modification_time(self, fname):
		t_sec = os.stat(fname).st_mtime
		# Change time in s since epoch to struct_time

		# Change struct_time to string given by format arg
		return time.strftime("%b %d %H:%M", time.gmtime(t_sec))


	def get_mode(self, fname):
		perms="-"
		link=""
		#mode = int(oct(stat.S_IMODE(os.stat(l_file).st_mode)))
		mode = os.stat(fname).st_mode
		
		if stat.S_ISLNK(mode):
			perms = "l"
			link = os.readlink(fname)
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

	def get_file_owners(self, fname):
		uid = os.stat(fname).st_uid
		gid = os.stat(fname).st_gid
		
		user = pwd.getpwuid(uid)[0]
		group = grp.getgrgid(gid)[0]
		
		return (user, group)

	def get_file_size(self, fname):
		size = os.stat(fname).st_size
		return size


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