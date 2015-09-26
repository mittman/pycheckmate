class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.pieces = {}

    def add_piece(self, piece):
        self.pieces[piece.type] = piece
