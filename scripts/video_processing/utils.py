import os

def check_and_create(dir_path):
	print ("Checking: %s" % dir_path)
	if not os.path.isdir(dir_path):
		print ('Destination directory: %s does not exist, creating one' % dir_path)
		os.makedirs(dir_path)
	else:
		print ('Found directory: %s ' % dir_path)