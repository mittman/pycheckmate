#!/usr/bin/env python3

import os, sys, re
from Board import Board
from Game import Game
from Piece import Piece
from Player import Player


def test_file(board, game, player_x, player_y):
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
			num = 1
			for line in f:
				line = line.rstrip()
				line = line.split(', ')

				for i in range(len(line)):
					if re.match(r"x\.K\([1-8],[1-8]\)", line[i]):
						moveH, moveV = game.split_entry(line[i])
						game.add_or_move(board, player_x, 'K', 'x', moveH, moveV, num)
					elif re.match(r"x\.R\([1-8],[1-8]\)", line[i]):
						moveH, moveV = game.split_entry(line[i])
						game.add_or_move(board, player_x, 'R', 'x', moveH, moveV, num)
					elif re.match(r"y\.K\([1-8],[1-8]\)", line[i]):
						moveH, moveV = game.split_entry(line[i])
						game.add_or_move(board, player_y, 'K', 'y', moveH, moveV, num)
					else:
						print("ERROR: invalid entry from file")

				board.display()
				num += 1

	except ValueError: "cannot read file"
	f.close()


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
		player_x = Player('x')
		player_y = Player('y')
		b = Board(player_x, player_y)
		test_file(b, g, player_x, player_y)


def test_case():
    rook_x = Piece('R', 'x', 5, 7)
    king_x = Piece('K', 'x', 3, 5)
    king_y = Piece('K', 'y', 4, 3)

    # king_x = Piece('K', 'x', 3, 3)
    # rook_x = Piece('R', 'x', 5, 6)
    # king_y = Piece('K', 'y', 1, 1)

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
    b.move('x', 'R', 2, 5)
    b.display()

    # AI random moves test:
    for i in range(0, 101):
        b.ai_move(player_x)
        b.display()
        b.ai_move(player_y)
        b.display()


if __name__ == '__main__':
	interactive()
