class Piece:
    def __init__(self, piece_type, player_number, row=None, col=None):
        self.type = piece_type
        self.player = player_number
        self.row = row
        self.col = col
