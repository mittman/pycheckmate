from Board import Board
import pycheckmate

def main():
    b = Board()

    pycheckmate.game_type()
    pycheckmate.add_piece(b)
    b.display()

if __name__ == '__main__':
    main()
