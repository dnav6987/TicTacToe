from Constants import EMPTY, X, O, SIZE, WINNING_BOARDS

# TODO, none of the player logic should be here. the controller should take care of that, even the switching

class Game:
    def __init__(self):
        # the game board. all positions initially empty
        self.board = [[EMPTY for i in range(SIZE)] for j in range(SIZE)]

        self.num_moves = 0

    def get_position(self, x, y):
        return self.board[x][y]

    def set_position(self, player, x, y):
        # TODO maybe the checks should go in the controller, maybe not
        # is it a valid player?
        if player != X and player != O:
            return False
        # not on the board
        if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
            return False

        self.board[x][y] = player

        self.num_moves += 1

        return True

    def board_full1(self):
        return self.num_moves == SIZE**2

    # have we won (or tied)?
    def winner1(self):
        # does this board match a winning board?
        for position in WINNING_BOARDS:
            # which player is in each possible winning position
            players = [self.board[y][x] for x, y in position]

            # if only 1 player was in all three positions they've won
            if len(set(players)) == 1 and players[0] != EMPTY:
                return players[0]

        # game is not over
        return 0

    # have we won (or tied)?
    @staticmethod
    def winner(board):
        # does this board match a winning board?
        for position in WINNING_BOARDS:
            # which player is in each possible winning position
            players = [board[y][x] for x, y in position]

            # if only 1 player was in all three positions they've won
            if len(set(players)) == 1 and players[0] != EMPTY:
                return players[0]

        # game is not over
        return 0

    @staticmethod
    def board_full(board):
        for i in board:
            for j in i:
                if j == EMPTY:
                    return False

        return True

    @staticmethod
    def game_over(board):
        return (Game.winner(board) or Game.board_full(board))