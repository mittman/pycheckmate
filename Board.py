class Board:
    def __init__(self, player_one, player_two):
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
        self.player_x = player_one
        self.player_y = player_two

    def display(self):
        for p in self.player_x.pieces.values():
            self.state[p.row][p.col] = p.player + p.type
        for p in self.player_y.pieces.values():
            self.state[p.row][p.col] = p.player + p.type
        print('\n'.join(''.join(['{:3}'.format(item) for item in row]) for row in self.state))

    def add_piece(self, p):
        self.state[p.row][p.col] = p.player + p.type

    def move(self, player_id, piece_id, new_row, new_col):
        # Will need to separate AI player moves from human player moves here.
        # Player should be able to move rook in to a dangerous spot. AI should not.
        # Currently this function doesn't allow dangerous moves for anyone.
        if player_id == 'x':
            hero = self.player_x
            opponent = self.player_y
        else:   # Can safely assume player_id == 'y'
            hero = self.player_y
            opponent = self.player_x
        piece = hero.pieces[piece_id]

        if self.legal_move(piece, new_row, new_col) and \
                self.tile_is_safe(opponent, new_row, new_col):
                    # Here is where the distinction between AI and human needs to happen
                    self.state[piece.row][piece.col] = '*'
                    hero.pieces[piece_id].row = new_row
                    hero.pieces[piece_id].col = new_col
        else:
            print('\n\nIllegal move.', end='')

    def tile_is_safe(self, enemy, tile_row, tile_col):
        for p in enemy.pieces.values():
            if self.legal_move(p, tile_row, tile_col):
                return False
        return True

    def legal_move(self, piece, new_row, new_col):
        if new_row == piece.row and new_col == piece.col:     # piece unmoved, illegal move
            return False
        if not (1 <= new_row <= 8):                           # input out of bounds
            return False
        if not (1 <= new_col <= 8):
            return False

        if piece.type == 'R':
            if new_row == piece.row or new_col == piece.col:  # horizontal/vertical move
                if self.state[new_row][new_col] == '*':       # space unoccupied
                    return True

        elif piece.type == 'K':
            if self.is_adjacent_spot(piece.row, piece.col, new_row, new_col):
                ### Need a tedious out of bounds check here ###
                return True

        else:
            return False

    def is_adjacent_spot(self, row, col, new_row, new_col):
        # Return True if new coordinates are adjacent (horizontally,
        # vertically, or diagonally) to the old coordinates.
        if (new_row == (row + 1) or new_row == (row - 1) or
            new_col == (col - 1) or new_col == (col - 1)) and \
           (new_row < (row + 2) and new_col < (col + 2) and
            row < (new_col + 2) and col < (new_col + 2)):
            return True
        else:
            return False
