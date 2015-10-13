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
		if len(sys.argv) >= 2:
			if os.path.isfile(sys.argv[-1]):
				filename = sys.argv[-1]
			elif os.path.isfile("testCase.txt"):
				filename = "testCase.txt"
			else:
				File.error("Usage " + sys.argv[0] + " [ply] [file]")
				exit(1)
		# default filename
		elif os.path.isfile("testCase.txt"):
			filename = "testCase.txt"
		else:
			self.error("unable to find 'testCase.txt'")
			exit(1)
		return filename

	def test_file(board, game, player_x, player_y):
		io = File()
		filename = io.open_file()

		# open file
		try:
			with open(filename, 'r', 1) as f:
				num = 1
				for line in f:
					line = line.rstrip()
					line = line.split(', ')

					for i in range(len(line)):
						game.parse_entry(line[i], game, board, player_x, player_y, num)

					board.display()
					num += 1

		except ValueError: "cannot read file"
		f.close()

	def print(text):
		if stdout:
			print(text)
		# write to file
		if logfile:
			log.write(text + '\n')
			log.flush()

	def prompt(text):
		if stdout:
			print("\033[1m" + "> " + text + "\033[0m")
		# write to file
		if logfile:
			log.write("> " + text + '\n')
			log.flush()

	def debug(text):
		if debug:
			print("--> " + str(text))

	def error(text):
		print("\033[1;31m==> ERROR:\033[0m \033[1m" + text + "\033[0m")

	def close():
		log.close()
