class Piece:
    def __init__(self, piece_type, player_number, row=None, col=None):
        self.type = piece_type
        self.player = player_number
        self.row = row
        self.col = col
        self.prev_coords = (row, col)

    def undo_move(self):
        self.row = self.prev_coords[0]
        self.col = self.prev_coords[1]
