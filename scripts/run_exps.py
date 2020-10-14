import os
import time

def main():
	for i in range(3):
		print "running experiment: " + str(i + 1)
		os.system('sudo python mn_script.py')
		time.sleep(10)

main()
