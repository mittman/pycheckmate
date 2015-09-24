#!/usr/bin/env python3
import os, sys, re
from Board import Board
from Piece import Piece

def game_type():
	print("> WOULD YOU LIKE TO PLAY A GAME?")
	print("y) yes, start a new game")
	print("n) no, this is a test")
	mode = input("Select (y/N): ")

	print("> MAX NUMBER OF MOVES?")
	end = input("Input (default 35): ")

	if re.match(r"[Yy]|[Yy][Ee][Ss]", mode):
		print("> NEW GAME")
	else:
		print("> TEST MODE ACTIVATED")

	if not re.match(r"[1-99]", end):
		end = 35
	else:
		print("> NOTE: GAME ENDS IN " + end + " MOVES")

def add_piece(board):
	print("> ADD PIECE TO BOARD?")
	print("1) PlayerX King")
	print("2) PlayerX Rook")
	print("3) PlayerY King")
	print("4) nope")

	option = input("Select [1-4]: ")
	if re.match(r"[1-3]", option):
		move_piece(option, board)
		add_piece()

def move_piece(option, board):
	if option == str(1):
		piece = Piece('K', 'x')
	elif option == str(2):
		piece = Piece('R', 'x')
	elif option == str(3):
		piece = Piece('K', 'y')

	print("> STARTING POSITION FOR " + option + " ?")
	moveH = input("Horizontal [1-8]: ")
	moveV = input("Vertical [1-8]: ")

	if not re.match(r"[1-8]", moveH):
		print("ERROR: expected [1-8]")
		exit(1)
	if not re.match(r"[1-8]", moveV):
		print("ERROR: expected [1-8]")
		exit(2)
	
	board.add_piece(piece, int(moveH), int(moveV))
	
	print("> OK " + option + " to " + moveH + "-" + moveV)


# Call functions

