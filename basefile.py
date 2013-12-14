
import os, pwd, grp, stat

class Basefile(object):
	"""
	All the funcions which can be executed on a file should go here

	"""

	def __init__(self):
		print 'dont know what to initialize :)'

	def get_mode(self, l_file):
		perms="-"
		link=""
		mode = int(oct(stat.S_IMODE(os.stat(l_file).st_mode)))
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

	def get_file_owners(self, l_file):
		uid = os.stat(l_file).st_uid
		gid = os.stat(l_file).st_gid
		
		user = pwd.getpwuid(uid)[0]
		group = grp.getgrgid(gid)[0]
		
		return (user, group)

	def get_file_size(self, l_file):
		size = os.stat(l_file).st_size
		return size

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

		for l_file in l_files:
			perms, link = self.get_mode(l_file)
			user, grp = self.get_file_owners(l_file)
			size = self.get_file_size(l_file)
			print perms, user, grp, size, l_file
		

class just_file(Basefile):

	def stdout(self):
		l_files = self.l()
					
if __name__ == '__main__':
	obj1 = just_file()
	obj1.stdout()
