#!/usr/bin/env python3

import os, sys, re
from Ai import Ai
from Board import Board
from File import File
from Game import Game
from Piece import Piece
from Player import Player

def interactive():
	g = Game()
	mode, end = g.game_type()
	end = int(end)

	if mode:	#mode is true means new game
		player_x = Player('x')
		player_y = Player('y')
		b = Board(player_x, player_y)
		ai = Ai(b)	#declared AI here for now -Brendon
		remain = [ 'PlayerX King', 'PlayerX Rook', 'PlayerY King' ]
		g.ask_piece(b, player_x, player_y, remain)

		localPlayer = input("Who am I PlayerX or PlayerY (x/y): ")
		if re.match(r"[Xx]", localPlayer):
			localPlayer = 'x'
		else:
			localPlayer = 'y'

		# if local player is playerX, PlayerX is our ai moves
		# PlayerY is opponents moves inputted by us
		if(localPlayer == 'x'):
			for i in range(0, end):
				b.ai_move(player_x)
				b.display()
				ai.opponent_move(player_y, b)
				# b.ai_move(player_y)
				b.display()
		else:
			for i in range(0, end):
				# b.ai_move(player_x)
				ai.opponent_move(player_x, b)
				b.display()
				b.ai_move(player_y)
				b.display()
		# AI random moves test:
		# for i in range(0, end):
		# 	b.ai_move(player_x)
		# 	b.display()
		# 	b.ai_move(player_y)
		# 	b.display()
	else:
		player_x = Player('x')
		player_y = Player('y')
		b = Board(player_x, player_y)
		File.test_file(b, g, player_x, player_y)

		# AI random moves test:
		for i in range(0, end):
			b.ai_move(player_x)
			b.display()
			b.ai_move(player_y)
			b.display()


# Note: function deprecated
def test_case():
	## old test case:
	test1()
	## new test case:
	test2()

def test1():
	player_x = Player('x')
	player_y = Player('y')

	king_x = Piece(player_x, 'K', 3, 5)
	rook_x = Piece(player_x, 'R', 5, 7)
	king_y = Piece(player_y, 'K', 4, 3)

	player_x.add_piece(rook_x)
	player_x.add_piece(king_x)
	player_y.add_piece(king_y)

	b = Board(player_x, player_y)
	b.display()

	# legal moves test:
	b.player_move(player_x, 'R', 5, 5)
	b.display()
	b.player_move(player_x, 'K', 4, 5)
	b.display()
	b.player_move(player_y, 'K', 3, 3)
	b.display()

	# illegal moves test:
	b.player_move(player_y, 'K', 3, 4)
	b.display()
	b.player_move(player_x, 'R', 2, 5)
	b.display()

	# AI random moves test:
	for i in range(0, 101):
		b.ai_move(player_x)
		b.display()
		b.ai_move(player_y)
		b.display()

def test2():
	player_x = Player('x')
	player_y = Player('y')

	king_x = Piece(player_x, 'K', 5, 5)
	rook_x = Piece(player_x, 'R', 8, 5)
	king_y = Piece(player_y, 'K', 6, 7)


	player_x.add_piece(rook_x)
	player_x.add_piece(king_x)
	player_y.add_piece(king_y)

	b = Board(player_x, player_y)
	b.display()

	ai = Ai(6)
	for i in range(35):
		ai.move(b, player_x)
		b.display()
		ai.move(b, player_y)
		b.display()
		# row, col = input('R,C:')
		# b.player_move(player_y, king_y, row, col)
		# b.display()
	# ai.create_tree(b, player_x)
	# ai.create_tree(b, player_y)
	# ai.display_tree(ai.root_node)
	# ai.bfs()
	print(ai.number_of_states)

if __name__ == '__main__':
	try:
		#test2()
		#test_case()
		interactive()
	except KeyboardInterrupt:
		print("\nExiting...")
		File.close()
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

	File.close()
