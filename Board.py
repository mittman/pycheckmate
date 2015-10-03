import random

class Board:
    def __init__(self, player_one, player_two):
        self.turn = 1
        self.state = [['         Turn: ', ''],
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
        self.move_log = ''

    def display(self):
        for p in self.player_x.pieces.values():
            self.state[p.row][p.col] = p.player + p.type
        for p in self.player_y.pieces.values():
            self.state[p.row][p.col] = p.player + p.type
        self.state[0][1] = str(self.turn)
        print('\n'.join(''.join(['{:3}'.format(item) for item in row]) for row in self.state))
        print(self.move_log)

    def move(self, player_id, piece_id, new_row, new_col):
        if player_id == 'x':
            hero = self.player_x
            opponent = self.player_y
        else:   # Can safely assume player_id == 'y'
            hero = self.player_y
            opponent = self.player_x
        piece = hero.pieces[piece_id]

        if piece_id == 'K' and not self.tile_is_safe(opponent, new_row, new_col):
            print('\nIllegal move.')
        elif not self.legal_move(piece, new_row, new_col):
            print('\nIllegal move.')
        else:
            # If playerY eats playerX's rook:
            if ('R' in self.player_x.pieces and
                new_row == self.player_x.pieces['R'].row and
                new_col == self.player_x.pieces['R'].col):
                    del self.player_x.pieces['R']
            # Move piece:
            self.state[piece.row][piece.col] = '*'
            hero.pieces[piece_id].row = new_row
            hero.pieces[piece_id].col = new_col

            self.turn += 1

        self.move_log = piece.player + piece.type + ' to ' + str(new_row) + ',' + str(new_col)

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
            if (new_row == piece.row or new_col == piece.col and    # horizontal/vertical move
                self.state[new_row][new_col] == '*' and             # space unoccupied
                self.is_clear_path(piece.row, piece.col, new_row, new_col)):
                    return True

        elif piece.type == 'K':
            if (self.is_adjacent_spot(piece.row, piece.col, new_row, new_col) and
                self.state[new_row][new_col][0] != piece.player):   # unoccupied by ally
                return True

        else:
            return False

    def is_adjacent_spot(self, row, col, new_row, new_col):
        # Return True if new coordinates are adjacent (horizontally,
        # vertically, or diagonally) to the old coordinates.
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (new_row, new_col) == (r, c):
                    return True
        return False

    def is_clear_path(self, from_row, from_col, to_row, to_col):
        # Check rook's path to make sure there are no obstacles in its way
        if to_row > from_row:       # moving horizontally to the right
            i = from_row + 1
            while i < to_row:
                if self.state[i][from_col] != '*':
                    return False
                i += 1
        elif to_row < from_row:     # moving horizontally to the left
            i = from_row - 1
            while i > to_row:
                if self.state[i][from_col] != '*':
                    return False
                i -= 1
        elif to_col > from_col:     # moving vertically up
            i = from_col + 1
            while i < to_col:
                if self.state[from_row][i] != '*':
                    return False
                i += 1
        else:                       # to_col < from_col; moving down
            i = from_col - 1
            while i > to_col:
                if self.state[from_row][i] != '*':
                    return False
                i -= 1
        return True

    def ai_move(self, player):
        if player.id == 'x':
            key = random.randint(0, 1)
            if key == 0 or 'R' not in player.pieces:
                piece = player.pieces['K']
            else:
                piece = player.pieces['R']
        else:
            piece = player.pieces['K']

        legal_moves = self.find_legal_moves(player, piece)

        ### if len(legal_moves) == 0: *CHECKMATE OR TIE* ###
        if len(legal_moves) == 1:
            new_destination = legal_moves[0]
        else:
            new_destination = legal_moves[random.randint(0, len(legal_moves) - 1)]

        # move:
        self.state[piece.row][piece.col] = '*'
        player.pieces[piece.type].row = new_destination[0]
        player.pieces[piece.type].col = new_destination[1]
        self.turn += 1

        self.move_log = piece.player + piece.type + ' to ' + \
                        str(new_destination[0]) + ',' + str(new_destination[1])

    def find_legal_moves(self, player, piece):
        opponent = self.player_y if player.id == 'x' else self.player_x

        legal_tiles = []
        if piece.type == 'R':
            for r in range(1, 9):
                if (self.legal_move(piece, r, piece.col) and
                    self.tile_is_safe(opponent, r, piece.col)):
                        legal_tiles.append((r, piece.col))
            for c in range(1, 9):
                if (self.legal_move(piece, piece.row, c) and
                    self.tile_is_safe(opponent, piece.row, c)):
                        legal_tiles.append((piece.row, c))
        else:       # piece = king
            for r in range(piece.row - 1, piece.row + 2):
                for c in range(piece.col - 1, piece.col + 2):
                    if (self.legal_move(piece, r, c) and
                        self.tile_is_safe(opponent, r, c)):
                            legal_tiles.append((r, c))
        return legal_tiles
