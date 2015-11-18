SIZE = 3 # size of each dimension of the board (3X3 board)

# Enumeration for possible states of a board position
O = -1
EMPTY = 0
X = 1

# cast enumerated types to strings
STRINGS = {EMPTY : '', X : 'X', O : 'O'}

# possible winning combinations
WINNING_BOARDS = (
    # horizontals
    ((0,0), (1,0), (2,0)),
    ((0,1), (1,1), (2,1)),
    ((0,2), (1,2), (2,2)),
    # verticals
    ((0,0), (0,1), (0,2)),
    ((1,0), (1,1), (1,2)),
    ((2,0), (2,1), (2,2)),
    # diagonals
    ((0,0), (1,1), (2,2)),
    ((2,0), (1,1), (0,2))
)