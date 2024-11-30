class Piece:
    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color

    def move(self, new_row, new_column):
        self.row = new_row
        self.column = new_column

class Knight(Piece):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.sign = 'k'

class Bishop(Piece):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.sign = 'b'

class Rook(Piece):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.sign = 'r'

class Queen(Piece):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.sign = 'q'

class King(Piece):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.sign = 'K'

class Pawn(Piece):
    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.sign = 'p'
