class Piece:
    def __init__(self, piece_type, player_number, col=None, row=None):
        self.type = piece_type
        self.player = player_number
        self.row = row
        self.col = col
