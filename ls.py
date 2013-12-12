#!/usr/bin/python

import sys, stat, os
import locale, getopt

#inode=0
def locale_sort(files):
	# Locale sensitive files sort
	locale.setlocale(locale.LC_ALL,'')
 	files.sort(locale.strcoll) # in place file sort
 	return files

def list_out_files():
	for filename in files:
		print filename

def get_inode(filename):
	# inode option
	try:
		st = os.stat(filename)
	except IOERROR:
		print "Failed to get information about the file", filename
	else:
		inode = st.st_ino
		return inode

def display(some_list):
	print some_list
		

# files is defined and contains all non hidden files
files = os.listdir(".")

files = [ filename for filename in files if filename[0]!='.' ] # Don't show hidden files
files = locale_sort(files)


if len(sys.argv) == 1:
	# No path given, list directories only
	list_out_files()

else:
	opts, args = getopt.getopt(sys.argv[1:], "ali")
	for o, a in opts:
		if o in ("-a", "--all"):
			hidden = 1 # Set the flag for option
		elif o in ("-l"):
			listing = 1
		elif o in ("-i","--inode"):
			inode = 1

# Should all the options flag be a list, so that I can traverse through the list to see 
# what all options are set and execute relevant functions and format output accordingly

# We need a output function which formats the output generated by variosu option funstions
# and on receiving their output should generate the final output	

if inode == 1:
	inode_num = [get_inode(filename) for filename in files ]
	display(inode_num)



		
