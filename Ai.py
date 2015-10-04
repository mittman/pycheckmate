from Board import Board
from Player import Player
from Piece import Piece
import copy

INFINITY = 9999999

class Ai:
    def __init__(self, _board, ply_level=5):
        self.board = _board
        self.ply = ply_level


    def move(self, player):
        if player.id == 'x':
            move = self.best_move_x(player)
        else:
            move = self.best_move_y(player)
        if move is None:
            ### GAME OVER, either tie or mate ###
            print('game over, do something')

        

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
