#!/usr/bin/env python3

import os, sys, re
from Board import Board
from File import File
from Game import Game
from Piece import Piece
from Player import Player


def test_file(board, game, player_x, player_y):
	filename = File.open_file()

	# open file
	try:
		with open(filename, 'r', 1) as f:
			num = 1
			for line in f:
				line = line.rstrip()
				line = line.split(', ')

				for i in range(len(line)):
					game.parse_entry(line[i], game, board, player_x, player_y, num)

				board.display()
				num += 1

	except ValueError: "cannot read file"
	f.close()


def interactive():
	g = Game()
	mode, end = g.game_type()
	end = int(end)

	if mode:
		player_x = Player('x')
		player_y = Player('y')
		b = Board(player_x, player_y)
		remain = [ 'PlayerX King', 'PlayerX Rook', 'PlayerY King' ]
		g.ask_piece(b, player_x, player_y, remain)

	    # AI random moves test:
		for i in range(0, end):
		    b.ai_move(player_x)
		    b.display()
		    b.ai_move(player_y)
		    b.display()
	else:
		player_x = Player('x')
		player_y = Player('y')
		b = Board(player_x, player_y)
		test_file(b, g, player_x, player_y)

	    # AI random moves test:
		for i in range(0, end):
		    b.ai_move(player_x)
		    b.display()
		    b.ai_move(player_y)
		    b.display()


def test_case():
    king_x = Piece('K', 'x', 3, 5)
    rook_x = Piece('R', 'x', 5, 7)
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
    b.move('x', 'R', 2, 5)
    b.display()

    # AI random moves test:
    for i in range(0, 101):
        b.ai_move(player_x)
        b.display()
        b.ai_move(player_y)
        b.display()


if __name__ == '__main__':
	#test_case()
	interactive()
