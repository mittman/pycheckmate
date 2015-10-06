from Board import Board
from File import File
from Player import Player
from Piece import Piece
import re
import copy

INFINITY = 9999999

class State:
	def __init__(self, state_board, moved_piece=None, move_coords=None, depth=0):
		self.board = state_board
		self.piece_to_move = moved_piece
		self.new_coords = move_coords
		self.children_nodes = []
		self.ply_level = depth + 1


class Ai:
	def __init__(self, _board, ply_level=3):
		self.board = _board
		self.max_ply = ply_level
		self.known_states = set()
		self.root_node = State(self.board)
		
		self.number_of_states = 0
	
	    def create_tree(self, player):
        self.known_states.add(self.board.piece_positions)
        self.create_state_tree(self.board, player, 0, self.root_node)

    # Recursively create state tree to max ply
	def create_state_tree(self, board, player, depth, parent):
		if depth != self.max_ply:   # base case
			for p in player.pieces.values():
				for move in board.find_legal_moves(p):
					# create a new board as a potential new state
					test_board = copy.deepcopy(board)
					hero, villain = test_board.identify_players(player)
					test_piece = hero.pieces[p.type]
					test_board.make_move(hero, test_piece, move)
					if test_board.piece_positions not in self.known_states:
						self.known_states.add(board.piece_positions)
						# create new child state:
						new_state = State(test_board, test_piece, move, depth)
						##### Test:
						self.number_of_states += 1
						#print('PLY LEVEL ' + str(new_state.ply_level))
						#new_state.board.display()
						
						# create state tree for opponent's moves from this child state:
						self.create_state_tree(test_board, villain, depth + 1, new_state)
						
						# add this new state to its parent
						parent.children_nodes.append(new_state)
				
				    # undo move from parent board:
				    # board.undo_move(p)


	def display_tree(self, state):
		if not state.children_nodes:  # children nodes are empty
			print('PLY LEVEL ' + str(state.ply_level))
			state.board.display()
		else:
			for i in range(0, len(state.children_nodes)):
				self.display_tree(state.children_nodes[i])
			print('\n\n')
			print('PLY LEVEL ' + str(state.ply_level))
			state.board.display()

	def opponent_move(self,player,board):
		if player.id == 'x':
			piece_name = input('Would you like to move the king or the rook? (r/k)')
			if re.match(r"[Kk]", piece_name) :
				piece = player.pieces['K']
			else:
				piece = player.pieces['R']
		else:
			piece = player.pieces['K']

		legal_moves = board.find_legal_moves(piece)

		for move in legal_moves:	#put X's where valid moves are
			horizontal, vertical = move
			board.state[horizontal][vertical] = 'X'

		board.display()
		horizontal= int(input('Select which coordinate you would like to move to (horizontal):'))	#TODO: input validation
		vertical= int(input('Select which coordinate you would like to move to (vertical):'))

		for move in legal_moves:	#put *'s back where X's were
			temp_hor, temp_vert = move
			board.state[temp_hor][temp_vert] = '*'
		board.make_move(player,piece, (horizontal, vertical))

		board.move_log = piece.player + piece.type + ' to ' + \
						str(horizontal) + ',' + str(vertical)


	def move(self, player):
		if player.id == 'x':
			move = self.best_move_x(player)
		else:
			move = self.best_move_y(player)
		if move is None:
			### GAME OVER, either tie or mate ###
			File.prompt('game over, do something')

		

	def best_move_x(self, plyr):
		mini = INFINITY
		best = None
		for p in plyr.pieces:
			for move in self.board.find_legal_moves(p):
				self.board.make_move(p, move)
				move_value = self.mini_value()
				if move_value < mini:
					mini = move_value
					best = move
				p.undo_move()
		return best

	def best_move_y(self, plyr):
		maxi = -INFINITY
		best = None
		for p in plyr.pieces:
			for move in self.board.find_legal_moves(p):
				self.board.make_move(p, move)
				move_value = self.max_value()
				if move_value > maxi:
					maxi = move_value
					best = move
				p.undo_move()
		return best


	# Return the value that represents the shortest distance
	# from player_y's king to the closest corner
	def mini_value(self):
		y_king_coords = (self.board.player_y.pieces['K'].row,
						 self.board.player_y.pieces['K'].col)

		corner_distance = min(min(self.distance(y_king_coords, (1, 1)),
								  self.distance(y_king_coords, (1, 8))),
							  min(self.distance(y_king_coords, (8, 1)),
								  self.distance(y_king_coords, (8, 8))))

		return corner_distance

	# Return the value that represents the longest distance
	# from player_y's king to the closest corner
	def max_value(self):
		y_king_coords = (self.board.player_y.pieces['K'].row,
						 self.board.player_y.pieces['K'].col)

		corner_distance = max(max(self.distance(y_king_coords, (1, 1)),
								  self.distance(y_king_coords, (1, 8))),
							  max(self.distance(y_king_coords, (8, 1)),
								  self.distance(y_king_coords, (8, 8))))

		return corner_distance

	# Return distance between two points
	def distance(self, p1, p2):
		x = p1[0] - p2[0]
		y = p1[1] - p2[1]
		hypotenuse = (x**2 + y**2)**.5   # a^2 = b^2 + c^2
		return hypotenuse
