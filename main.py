#!/usr/bin/env python3

import os, sys, re
from Ai import Ai
from Board import Board
from File import File
from Game import Game
from Piece import Piece
from Player import Player


def test_file(board, game, player_x, player_y):
	io = File()
	filename = io.open_file()

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

	if mode:	#mode is true means new game
		localPlayer = input("Are you playing as PlayerX or PlayerY (x/y): ")	#Maybe change wording later -Brendon
		if re.match(r"[Xx]", localPlayer):
			localPlayer = 'x'
		else:
			localPlayer = 'y'
		player_x = Player('x')
		player_y = Player('y')
		b = Board(player_x, player_y)
		ai = Ai(b)	#declared AI here for now -Brendon
		remain = [ 'PlayerX King', 'PlayerX Rook', 'PlayerY King' ]
		g.ask_piece(b, player_x, player_y, remain)

		if(localPlayer == 'x'):	#if local player is playerX, PlayerX is our ai moves, PlayerY is opponents moves inputted by us
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
		test_file(b, g, player_x, player_y)

		# AI random moves test:
		for i in range(0, end):
			b.ai_move(player_x)
			b.display()
			b.ai_move(player_y)
			b.display()


# Note: function deprecated
def test_case():
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


if __name__ == '__main__':
	try:
		#test_case()
		interactive()
	except KeyboardInterrupt:
		print("\nExiting...")
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
