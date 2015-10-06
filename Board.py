import random
from File import File

class Board:
	def __init__(self, player_one, player_two):
		self.state = [['', '		 ', 'Turn: ', ''],
					  ['1', '*', '*', '*', '*', '*', '*', '*', '*'],
					  ['2', '*', '*', '*', '*', '*', '*', '*', '*'],
					  ['3', '*', '*', '*', '*', '*', '*', '*', '*'],
					  ['4', '*', '*', '*', '*', '*', '*', '*', '*'],
					  ['5', '*', '*', '*', '*', '*', '*', '*', '*'],
					  ['6', '*', '*', '*', '*', '*', '*', '*', '*'],
					  ['7', '*', '*', '*', '*', '*', '*', '*', '*'],
					  ['8', '*', '*', '*', '*', '*', '*', '*', '*'],
					  [' ', '1', '2', '3', '4', '5', '6', '7', '8']]
		self.player_x = player_one
		self.player_y = player_two
		self.move_log = ''
		# piece_positions acts as a key to this current state:
		self.piece_positions = self.new_positions()

	def display(self):
		for p in self.player_x.pieces.values():
			self.state[p.row][p.col] = p.player + p.type
		for p in self.player_y.pieces.values():
			self.state[p.row][p.col] = p.player + p.type
		if self.move_log == '':
			self.state[0][3] = str(0)
		else:
			self.state[0][3] = str(self.player_x.turn)
		File.print('')
		File.print('\n'.join(''.join(['{:3}'.format(item) for item in row]) for row in self.state))
		File.print(self.move_log)

	def player_move(self, player, piece_id, new_row, new_col):
		hero, opponent = self.identify_players(player)
		piece = hero.pieces[piece_id]
		self.state[piece.row][piece.col] = '*'

		if piece_id == 'K' and not self.tile_is_safe(opponent, new_row, new_col):
			print('\n')
			File.error("Illegal move.")
			self.state[piece.row][piece.col] = piece.player + piece.type
		elif not self.legal_move(piece, new_row, new_col):
			print('\n')
			File.error("Illegal move.")
			self.state[piece.row][piece.col] = piece.player + piece.type
		else:
			self.make_move(player, piece, (new_row, new_col))

		self.move_log = piece.player + piece.type + ' to ' + str(new_row) + ',' + str(new_col)

	def make_move(self, player, piece, new_coords):
		new_row = new_coords[0]
		new_col = new_coords[1]
		# If playerY eats playerX's rook:
		if ('R' in self.player_x.pieces and
			new_row == self.player_x.pieces['R'].row and \
			new_col == self.player_x.pieces['R'].col):
				del self.player_x.pieces['R']

		self.state[piece.row][piece.col] = '*'
		piece.prev_coords = (piece.row, piece.col)
		piece.row = new_coords[0]
		piece.col = new_coords[1]
		self.state[0][0] = "player" + piece.player.upper()
		self.state[piece.row][piece.col] = piece.player + piece.type
		self.piece_positions = self.new_positions()
		player.turn += 1

	def tile_is_safe(self, enemy, tile_row, tile_col):
		# Make new tile temporarily empty:
		owner = self.state[tile_row][tile_col]
		self.state[tile_row][tile_col] = '*'

		# Make sure it's safe:
		for p in enemy.pieces.values():
			if self.legal_move(p, tile_row, tile_col):
				return False

		self.state[tile_row][tile_col] = owner
		return True

	def legal_move(self, piece, new_row, new_col):
		if new_row == piece.row and new_col == piece.col:	 # piece unmoved, illegal move
			return False
		if not (1 <= new_row <= 8):						   # input out of bounds
			return False
		if not (1 <= new_col <= 8):
			return False

		if piece.type == 'R':
			if ((new_row == piece.row or new_col == piece.col) and	  # horizontal/vertical move
				self.state[new_row][new_col][0] != piece.player and   # space unoccupied by ally
				self.is_clear_path(piece.row, piece.col, new_row, new_col)):
					return True

		elif piece.type == 'K':
			if (self.is_adjacent_spot(piece.row, piece.col, new_row, new_col) and
				self.state[new_row][new_col][0] != piece.player):   # unoccupied by ally
				return True

		else:
			return False

	def is_adjacent_spot(self, row, col, new_row, new_col):
		# Return True if new coordinates are adjacent (horizontally,
		# vertically, or diagonally) to the old coordinates.
		for r in range(row - 1, row + 2):
			for c in range(col - 1, col + 2):
				if (new_row, new_col) == (r, c):
					return True
		return False

	def is_clear_path(self, from_row, from_col, to_row, to_col):
		# Check rook's path to make sure there are no obstacles in its way
		if to_row > from_row:	   # moving horizontally to the right
			i = from_row + 1
			while i < to_row:
				if self.state[i][from_col] != '*':
					return False
				i += 1
		elif to_row < from_row:	 # moving horizontally to the left
			i = from_row - 1
			while i > to_row:
				if self.state[i][from_col] != '*':
					return False
				i -= 1
		elif to_col > from_col:	 # moving vertically up
			i = from_col + 1
			while i < to_col:
				if self.state[from_row][i] != '*':
					return False
				i += 1
		else:					   # to_col < from_col; moving down
			i = from_col - 1
			while i > to_col:
				if self.state[from_row][i] != '*':
					return False
				i -= 1
		return True

	def ai_move(self, player):
		if player.id == 'x':
			key = random.randint(0, 1)
			if key == 0 or 'R' not in player.pieces:
				piece = player.pieces['K']
			else:
				piece = player.pieces['R']
		else:
			piece = player.pieces['K']

		legal_moves = self.find_legal_moves(piece)

		### if len(legal_moves) == 0: *CHECKMATE OR TIE* ###
		if len(legal_moves) == 0:
			File.print("game over")
			exit(0)
		if len(legal_moves) == 1:
			new_destination = legal_moves[0]
		else:
			new_destination = legal_moves[random.randint(0, len(legal_moves) - 1)]

		# move:
		self.make_move(player, piece, (new_destination[0], new_destination[1]))

		self.move_log = piece.player + piece.type + ' to ' + \
						str(new_destination[0]) + ',' + str(new_destination[1])



	def find_legal_moves(self, piece):
		opponent = self.player_y if piece.player == 'x' else self.player_x
		self.state[piece.row][piece.col] = '*'

		legal_tiles = []
		if piece.type == 'R':
			for r in range(1, 9):
				if (self.legal_move(piece, r, piece.col) and
					self.tile_is_safe(opponent, r, piece.col)):
						legal_tiles.append((r, piece.col))
			for c in range(1, 9):
				if (self.legal_move(piece, piece.row, c) and
					self.tile_is_safe(opponent, piece.row, c)):
						legal_tiles.append((piece.row, c))
		else:   # piece = king
			for r in range(piece.row - 1, piece.row + 2):
				for c in range(piece.col - 1, piece.col + 2):
					if (self.legal_move(piece, r, c) and
						self.tile_is_safe(opponent, r, c)):
							legal_tiles.append((r, c))
							
		self.state[piece.row][piece.col] = piece.player + piece.type
		return legal_tiles

	def identify_players(self, current_player):
		if current_player.id == 'x':
			hero = self.player_x
			villain = self.player_y
		else:   # Can safely assume player_id == 'y'
			hero = self.player_y
			villain = self.player_x
		return hero, villain
		
	# Function to just serve as a key to this current state
	def new_positions(self):
		# Terrible way of doing this, but whatever
		key = ''
		if 'K' not in self.player_x.pieces:
			return key
		if 'R' in self.player_x.pieces:
			key = 'xR' + str(self.player_x.pieces['R'].row) + str(self.player_x.pieces['R'].col)
		key += 'xK' + str(self.player_x.pieces['K'].row) + str(self.player_x.pieces['K'].col)
		key += 'yK' + str(self.player_y.pieces['K'].row) + str(self.player_y.pieces['K'].col)
		return key

	def undo_move(self, piece):
		self.state[piece.row][piece.col] = '*'
		piece.undo_move()
		self.state[piece.row][piece.col] = piece.player + piece.type
