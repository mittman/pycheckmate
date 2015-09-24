class Board:
    def __init__(self):
        self.state = [['\n'],
                      ['1', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['2', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['3', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['4', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['5', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['6', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['7', '*', '*', '*', '*', '*', '*', '*', '*'],
                      ['8', '*', '*', '*', '*', '*', '*', '*', '*'],
                      [' ', '1', '2', '3', '4', '5', '6', '7', '8']]
        #self.danger_zone = []       # all the coordinates that are under attack on the board

    def display(self):
        print('\n'.join(''.join(['{:3}'.format(item) for item in row]) for row in self.state))

    def add_piece(self, piece, row, col):
        piece.row = row
        piece.col = col
        #self.update_danger_zone(piece)
        self.state[row][col] = str(piece.player) + piece.type

    #def update_danger_zone(self, piece):
        # create new danger zone (for checking purposes)
        #if piece.type == 'R':


    def legal_move(self, piece, new_row, new_col):
        if new_row == piece.row and new_col == piece.col:     # piece unmoved, illegal move
            return False
        if not (1 <= new_row <= 16):                          # input out of bounds
            return False
        if not (1 <= new_col <= 16):
            return False

        if piece.type == 'R':
            if new_row == piece.row or new_col == piece.col:  # horizontal/vertical move
                if self.state[new_row][new_col] == '*':       # space unoccupied
                    return True

        elif piece.type == 'K':
            if self.is_adjacent_spot(piece.row, piece.col, new_row, new_col) and \
               self.state[new_row][new_col] == '*':    ### needs a player check to see if player 2's
                                                       ### king can take the opponent's rook
                    return True

        else:
            return False

    def is_adjacent_spot(self, row, col, new_row, new_col):
        # Return True if new coordinates are adjacent (horizontally,
        # vertically, or diagonally) to the old coordinates.
        if (new_row == (row + 1) or new_col == (col + 1) or
            new_row == (row - 1) or new_col == (col - 1)) and \
           (new_row < (row + 2) and new_col < (col + 2)):
            return True
        else:
            return False
