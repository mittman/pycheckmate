import re
from Piece import Piece

class Game:
	def game_type(self):
		mode = None
		end = 0

		print("> SHALL WE PLAY A GAME?")
		print("y) yes, start a new game")
		print("n) no, this is a test")
		mode = input("Select (y/N): ")

		print("> MAX NUMBER OF MOVES?")
		end = input("Input (default 35): ")

		if re.match(r"[Yy]|YES|yes", mode):
			print("> NEW GAME")
			mode = True
		else:
			print("> TEST MODE ACTIVATED")
			mode = False

		if not re.match(r"[1-99]", end):
			end = 35
		else:
			print("> NOTE: GAME ENDS IN " + end + " MOVES")

		return mode, end

	def ask_piece(self, board, player_x, player_y, remain):
		print("> ADD PIECE TO BOARD?")

		i = 0
		for p in remain:
			i += 1
			print(str(i) + ") " + p)
		print(str(i+1) + ") quit")

		n = len(remain)
		option = input("Select [1-" + str(n+1) + "]: ")
		try:
			option = int(option)
		except ValueError: self.ask_piece(board, player_x, player_y, remain)

		if option == n + 1:
			pass
		elif option <= n and option > 0 and n > 1:
			print("debug 1")
			piece_name = remain[option-1]
			self.insert_piece(board, piece_name, player_x, player_y)
			remain.pop(option-1)
			self.ask_piece(board, player_x, player_y, remain)
		elif option <= n and option > 0:
			print("debug 2")
			piece_name = remain[option-1]
			self.insert_piece(board, piece_name, player_x, player_y)
			remain.pop(option-1)
		else:
			print("Try again")
			self.ask_piece(board, player_x, player_y, remain)

	def insert_piece(self, board, piece_name, player_x, player_y):
		print("> STARTING POSITION FOR " + piece_name + " ?")

		moveH = input("Horizontal [1-8]: ")
		moveH = int(moveH)
		while moveH < 1 or moveH > 8:
			print("ERROR: expected [1-8]")
			moveH = input("Horizontal [1-8]: ")
			moveH = int(moveH)

		moveV = input("Vertical [1-8]: ")
		moveV = int(moveV)
		while moveV < 1 or moveV > 8:
			print("ERROR: expected [1-8]")
			moveV = input("Vertical [1-8]: ")
			moveV = int(moveV)

		if board.state[moveH][moveV] != '*':
			print("ERROR: space occupied")
			exit(2)

		if piece_name == "PlayerX King":
			piece_id = Piece('K', 'x', moveH, moveV)
			player_x.add_piece(piece_id)
		elif piece_name == "PlayerX Rook":
			piece_id = Piece('R', 'x', moveH, moveV)
			player_x.add_piece(piece_id)
		elif piece_name == "PlayerY King":
			piece_id = Piece('K', 'y', moveH, moveV)
			player_y.add_piece(piece_id)
		else:
			print("ERROR: expected valid piece")
			exit(3)

		print("> OK " + piece_name + " to " + str(moveH) + "-" + str(moveV))

		board.display()
