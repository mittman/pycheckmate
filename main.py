from Board import Board
from Piece import Piece
from Player import Player

def main():
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
    main()
