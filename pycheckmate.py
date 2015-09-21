#!/usr/bin/env python3
import os, sys, re

tile = [['*' for x in range(16)] for x in range(16)]

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

if not re.match(r"[1-99]", mode):
	end = 35
else:
	print("> NOTE: GAME ENDS IN " + end + " MOVES")

tile[0][0] = "WK"
tile[15][0] = "BK"
tile[15][5] = "BR"

print("> ADD PIECE TO BOARD?")
print("1) PlayerX King")
print("2) PlayerX Rook")
print("3) PlayerY King")
print("4) nope")
piece = input("Select [1-4]: ")

if piece == 1:
	piece = "xk"
elif piece == 2:
	piece = "xr"
elif piece == 3:
	piece = "yk"

if not re.match(r"[1-8]", moveH):
	print("ERROR: expected [1-8]")
	exit(1)
if not re.match(r"[1-8]", moveV):
	print("ERROR: expected [1-8]")
	exit(2)
