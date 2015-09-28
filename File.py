import os, sys

class File:
	def open_file():
		# parse optional parameter
		if len(sys.argv) == 2:
			if os.path.isfile(sys.argv[1]):
				filename = sys.argv[1]
			else:
				print("USAGE: " + sys.argv[0] + " [file]")
				exit(1)
		# default filename
		elif os.path.isfile("testCase.txt"):
			filename = "testCase.txt"
		else:
			print("unable to find 'testCase.txt'")
			exit(1)
		return filename
