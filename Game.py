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

		n = len(remain)
		option = input("Select [1-" + str(n) + "]: ")
		try:
			option = int(option)
		except ValueError: self.ask_piece(board, player_x, player_y, remain)

		if option <= n and option > 0 and n > 1:
			piece_name = remain[option-1]
			self.insert_piece(board, piece_name, player_x, player_y)
			remain.pop(option-1)
			self.ask_piece(board, player_x, player_y, remain)
		elif option <= n and option > 0:
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
			piece_id = Piece(player_x, 'K', moveH, moveV)
			player_x.add_piece(piece_id)
		elif piece_name == "PlayerX Rook":
			piece_id = Piece(player_x, 'R', moveH, moveV)
			player_x.add_piece(piece_id)
		elif piece_name == "PlayerY King":
			piece_id = Piece(player_y, 'K', moveH, moveV)
			player_y.add_piece(piece_id)
		else:
			print("ERROR: expected valid piece")
			exit(3)

		print("> OK " + piece_name + " to " + str(moveH) + "-" + str(moveV))
		board.display()


	def split_entry(self, entry):
		coordinates = entry.split(',')
		moveH = coordinates[0]
		moveH = moveH[-1]
		moveH = int(moveH)
		moveV = coordinates[1]
		moveV = moveV[0]
		moveV = int(moveV)
		return moveH, moveV

	def parse_entry(self, entry, game, board, player_x, player_y, num):
		if re.match(r"x\.K\([1-8],[1-8]\)", entry):
			moveH, moveV = game.split_entry(entry)
			game.add_or_move(board, player_x, 'K', moveH, moveV, num)
		elif re.match(r"x\.R\([1-8],[1-8]\)", entry):
			moveH, moveV = game.split_entry(entry)
			game.add_or_move(board, player_x, 'R', moveH, moveV, num)
		elif re.match(r"y\.K\([1-8],[1-8]\)", entry):
			moveH, moveV = game.split_entry(entry)
			game.add_or_move(board, player_y, 'K', moveH, moveV, num)
		else:
			print("ERROR: invalid entry from file")

	def add_or_move(self, board, player, piece_id, moveH, moveV, num):
		if num == 1:
			new_piece = Piece(player, piece_id, moveH, moveV)
			if player.id == 'x':
				player.add_piece(new_piece)
			elif player.id == 'y':
				player.add_piece(new_piece)
			else:
				print("ERROR: invalid player")
		else:
			if board.state[moveH][moveV] != player.id + piece_id:
				print("\n\nMove " + player.id + piece_id + " to " + str(moveH) + "," + str(moveV))
				board.move(player, piece_id, moveH, moveV)
