from File import File
import re
import copy

INFINITY = 9999

class State:
	def __init__(self, state_board, moved_piece=None, move_coords=None, depth=0, parent=None):
		self.board = state_board
		self.piece_to_move = moved_piece
		self.new_coords = move_coords
		self.children_nodes = []
		self.ply_level = depth + 1
		self.value = None
		self.next_parent = parent
		self.prune = False


class Ai:
	def __init__(self, ply_level=3):
		self.max_ply = ply_level
		self.known_states = set()
		self.root_node = None
		
		self.number_of_states = 0
	
	def move(self, board, player):
		if not board.find_legal_moves(board.player_y.pieces['K']):
			print('GAME OVER')
		else:
			self.root_node = State(board)
			self.create_state_tree(board, player, 0, self.root_node)
			
		best_state = self.root_node.children_nodes[0]
		for s in self.root_node.children_nodes:
			if player.id == 'x':
				if s.value < best_state.value:
					best_state = s
			else:
				if s.value > best_state.value:
					best_state = s
		piece = player.pieces[best_state.piece_to_move.type]
		board.make_move(player, piece, best_state.new_coords)
	
	# This create tree is just for test cases. Main one below is called in move()
	def create_tree(self, board, player):
		self.root_node = State(board)
		self.known_states.add(self.board.piece_positions)
		self.create_state_tree(self.board, player, 0, self.root_node, True)

	# Create state tree up to max play. Pretty much completely indecipherable now
	def create_state_tree(self, board, player, depth, parent, is_min):
		if depth != self.max_ply:   # base case
			for p in player.pieces.values():
				moves = board.find_legal_moves(p)
				if not moves:   # empty list - can only happen for player y
					# if currently not under check--tie situation, return INFINITY + depth
					if board.tile_is_safe(board.player_x, p.row, p.col):
						parent.value = self.assign_value(board, board.player_y, depth)
					else:   # else currently in checkmate, return -INFINITY + depth
						parent.value = self.assign_value(board, board.player_x, depth)
				for move in moves:
					if not parent.prune:
						# create a new board as a potential new state
						test_board = copy.deepcopy(board)
						hero, villain = test_board.identify_players(player)
						test_piece = hero.pieces[p.type]
						test_board.make_move(hero, test_piece, move)
						# create new child state:
						new_state = State(test_board, test_piece, move, depth, parent)
						self.number_of_states += 1

						# create state tree for opponent's moves from this child state:
						self.create_state_tree(test_board, villain, depth + 1, new_state, not is_min)

						####### MINIMAX HAPPENS HERE ########
						if new_state.value is not None:
							if is_min:
								if parent.value is None or new_state.value < parent.value:
									parent.value = new_state.value
							else:
								if parent.value is None or new_state.value > parent.value:
									parent.value = new_state.value
						####### ALPHA BETA PRUNING ########
						if (parent.next_parent is not None and
							parent.value is not None and parent.next_parent.value is not None):
								ancestor_vals = self.ancestor_values(parent)
								if is_min:  # parent = is_max
									for val in ancestor_vals:
										if parent.value >= val:
											parent.prune = True
								else:       # parent = is_min
									for val in ancestor_vals:
										if parent.value <= val:
											parent.prune = True

						# add this new state to its parent
						parent.children_nodes.append(new_state)
		else:   # Leaf node, assign value
			hero, villain = board.identify_players(player)
			parent.value = self.assign_value(board, villain, depth)

	def ancestor_values(self, state):
		if state.next_parent is None or state.next_parent.value is None:
			return []
		else:
			return [state.next_parent.value] + self.ancestor_values(state.next_parent)
			
	def bfs(self):
		opened = [self.root_node]
		closed = []
		while opened:
			node = opened[0]
			opened.pop(0)
			children = [x for x in node.children_nodes]
			closed.append(node)
			for c in children:
				opened.append(c)
				print('PLY LEVEL ' + str(c.ply_level))
				c.board.display()
				print(c.value)
			
	# If goal state has been reached, return (+/-)infinity, otherwise return minimax value
	def assign_value(self, board, player, depth):
		if not board.find_legal_moves(board.player_y.pieces['K']):  # no moves left for playerY
			return (depth + -INFINITY) if player.id == 'x' else (depth + INFINITY)
		else:
			return depth + self.value(board)

	# Return the value that represents the shortest distance
	# from player_y's king to the closest corner
	def value(self, board):
		y_king_coords = (board.player_y.pieces['K'].row,
						 board.player_y.pieces['K'].col)

		corner_distance = min(min(self.distance(y_king_coords, (1, 1)),
								  self.distance(y_king_coords, (1, 8))),
							  min(self.distance(y_king_coords, (8, 1)),
								  self.distance(y_king_coords, (8, 8))))

		return corner_distance
	
	# Return distance between two points
	def distance(self, p1, p2):
		x = p1[0] - p2[0]
		y = p1[1] - p2[1]
		hypotenuse = (x**2 + y**2)**.5   # a^2 = b^2 + c^2
		return hypotenuse

	def opponent_move(self, player, board):
		horizontal = 0
		vertical = 0
		if player.id == 'x':
			File.prompt("Move which PlayerX piece?")
			File.print("1) Rook")
			File.print("2) King")

			option = input("Select [1-2]: ")
			try:
				option = int(option)
			except ValueError:
				File.error("Try again")
				self.opponent_move(player, board)

			if option == 1:
				piece = player.pieces['R']
			elif option == 2:
				piece = player.pieces['K']
			else:
				File.error("Try again")
				self.opponent_move(player, board)
		else:
			piece = player.pieces['K']

		legal_moves = board.find_legal_moves(piece)

		for move in legal_moves:	#put X's where valid moves are
			horizontal, vertical = move
			board.state[horizontal][vertical] = '+'

		board.display()

		validInput = False
		while not validInput:
			if piece.type == 'K':
				name = "King"
			elif piece.type == 'R':
				name = "Rook"

			File.prompt("Move " + name + " to coordinates")
			horizontal= input("Horizontal [1-8]: ")
			vertical= input("Vertical [1-8]: ")
			try:	#validate input
				horizontal = int(horizontal)
				vertical = int(vertical)
			except ValueError: validInput = False
			for move in legal_moves:	#check if moves match a legal move
				temp_hor, temp_vert = move
				if horizontal == temp_hor and vertical == temp_vert:
					validInput = True
			if validInput != True:
				File.error("Please select a legal move.")


		for move in legal_moves:	#put *'s back where X's were
			temp_hor, temp_vert = move
			board.state[temp_hor][temp_vert] = '*'
		board.make_move(player,piece, (horizontal, vertical))

		board.move_log = piece.player + piece.type + ' to ' + \
						str(horizontal) + ',' + str(vertical)


