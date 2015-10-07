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
				moves = board.find_legal_moves(p)
				if not moves:   # empty list
					self.assign_value(board, player, depth)
				for move in moves:
					# create a new board as a potential new state
					test_board = copy.deepcopy(board)
					hero, villain = test_board.identify_players(player)
					test_piece = hero.pieces[p.type]
					test_board.make_move(hero, test_piece, move)
					# create new child state:
					new_state = State(test_board, test_piece, move, depth)
					self.number_of_states += 1

					# create state tree for opponent's moves from this child state:
					self.create_state_tree(test_board, villain, depth + 1, new_state)

					# add this new state to its parent
					parent.children_nodes.append(new_state)

					# undo move from parent board:
					# board.undo_move(p)
		else:   # Last ply-level state in tree
			self.assign_value(board, player, depth)

	def bfs(self):
		opened = [self.root_node]
		closed = []
		while opened:
			node = opened[0]
			opened.pop(0)
			## if X is a gola then return SUCCESS
			## else:
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
			return self.value(board)

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

