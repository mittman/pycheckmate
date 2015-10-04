import os, sys

debug = False
logfile = True
stdout = True

# open log file
try:
	log = open("gameResult.txt", 'w')
except PermissionError: "cannot write file"

class File:
	def open_file(self):
		# parse optional parameter
		if len(sys.argv) == 2:
			if os.path.isfile(sys.argv[1]):
				filename = sys.argv[1]
			else:
				File.error("Usage " + sys.argv[0] + " [file]")
				exit(1)
		# default filename
		elif os.path.isfile("testCase.txt"):
			filename = "testCase.txt"
		else:
			error("unable to find 'testCase.txt'")
			exit(1)
		return filename

	def print(text):
		if stdout:
			print(text)
		# write to file
		if logfile:
			log.write(text + '\n')

	def prompt(text):
		if stdout:
			print("\033[1m" + "> " + text + "\033[0m")
		# write to file
		if logfile:
			log.write("> " + text + '\n')

	def debug(text):
		if debug:
			print("--> " + text)

	def error(text):
		print("\033[1;31m==> ERROR:\033[0m \033[1m" + text + "\033[0m")
