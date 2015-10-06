from collections import OrderedDict

class Player:
	def __init__(self, player_id):
		self.id = player_id
		self.pieces = OrderedDict({})
		self.turn = 0

	def add_piece(self, piece):
		self.pieces[piece.type] = piece

	def plus(self, player):
		player.turn += 1
