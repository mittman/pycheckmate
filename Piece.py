class Piece:
    def __init__(self, player_number, piece_type, row=None, col=None):
        self.player = player_number.id
        self.type = piece_type
        self.row = row
        self.col = col
        self.prev_coords = (row, col)

    def undo_move(self):
        self.row = self.prev_coords[0]
        self.col = self.prev_coords[1]
