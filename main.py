#!/usr/bin/env python3

import os, sys
from Board import Board
from Game import Game
from Piece import Piece
from Player import Player


def test_file():
	# parse optional parameter
	if len(sys.argv) == 2:
		if os.path.isfile(sys.argv[1]):
			filename = sys.argv[1]
		else:
			print("USAGE: " + sys.argv[0] + " [file]")
			exit(1)
	# default filename
	elif os.path.isfile("testCase.txt"):
		filename = "testCase.txt"
	else:
		print("unable to find 'testCase.txt'")
		exit(1)

	# open file
	try:
		with open(filename, 'r', 1) as f:
			line = f.readlines(1)
			#line = line.rstrip('\n')
			print(line)
	except ValueError: "cannot read file"
	f.close()
## not finished

def interactive():
	g = Game()
	mode, end = g.game_type()

	if mode:
		player_x = Player('x')
		player_y = Player('y')
		b = Board(player_x, player_y)

		remain = [ 'PlayerX King', 'PlayerX Rook', 'PlayerY King' ]
		g.ask_piece(b, player_x, player_y, remain)
	else:
		test_case()

def test_case():
	rook_x = Piece('R', 'x', 5, 7)
	king_x = Piece('K', 'x', 3, 5)
	king_y = Piece('K', 'y', 4, 3)

	player_x = Player('x')
	player_y = Player('y')

	player_x.add_piece(rook_x)
	player_x.add_piece(king_x)
	player_y.add_piece(king_y)

	b = Board(player_x, player_y)
	b.display()

	# legal moves test:
	b.move('x', 'R', 5, 5)
	b.display()
	b.move('x', 'K', 4, 5)
	b.display()
	b.move('y', 'K', 3, 3)
	b.display()

	# illegal moves test:
	b.move('y', 'K', 3, 4)
	b.display()



if __name__ == '__main__':
	interactive()
