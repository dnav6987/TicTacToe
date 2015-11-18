from NeuralNetwork import NeuralNetwork
from Constants import SIZE, X, O, EMPTY
from GameState import Game
from copy import deepcopy

# todo trouble boards: poss losing board???
# -1 0 -1 1 1 -1 0 0 0
# [-1, 0, -1, 1, 1, -1, 0, 0, 0]

class LearningPlayer:
    def __init__(self):
        input_size = output_size = SIZE**2

        self.net = NeuralNetwork([input_size, 2*input_size, output_size])
        self.net.set_learning_rate(.002)
        self.net.set_momentum(.8)

        self.passed_moves = self.failed_moves = 0

        self.boards_file = 'known_boards.txt'
        self.load_known_boards()

    def make_move(self, player, board):
        inputs = [player*board[j][i] for i in range(SIZE) for j in range(SIZE)]

        if not inputs in self.known_boards: self.add_board(inputs);

        self.net.set_input(inputs)
        self.net.forward_propagate()
        output = self.net.get_output()

        while True:
            move = output.index(max(output))
            y = move/SIZE
            x = move%SIZE
        
            if board[x][y] == EMPTY:
                return move

            else:
                output[move] = -1

        return move

    def train_on_all_known_boards(self):
        self.passed_moves = self.failed_moves = 0

        perfect_player = PerfectPlayer(X)

        for board in self.known_boards:
            grid_board = [[0 for j in range(SIZE)] for i in range(SIZE)]
            
            for i in range(len(board)):
                grid_board[i%SIZE][i/SIZE] = board[i]

            correct_move = perfect_player.make_move(grid_board)
            # if board == [-1, 0, -1, 1, 1, -1, 0, 0, 0]: print correct_move

            self.train_move(X, grid_board, correct_move)

    def train_move(self, player, board, correct_move):
        my_move = self.make_move(1, board)

        if my_move == correct_move: self.passed_moves += 1

        else:
            self.failed_moves += 1

            expected_output = [0 for i in range(SIZE) for j in range(SIZE)]
            expected_output[correct_move] = 1

            self.net.back_propagate(expected_output)

        return my_move

    def add_board(self, board):
        if not len(board) == SIZE**2: raise IndexError('board is not 3x3')

        if board in self.known_boards: return

        else:
            self.known_boards.append(board)

            with open(self.boards_file, "a") as boards:
                boards.write('\n')
                boards.write(' '.join(str(i) for i in board))

    def load_known_boards(self):
        try:
            boards = open(self.boards_file)
        except IOError:
            print 'could not find known_boards.txt'


        self.known_boards = []

        for board in boards:
            this_board = board.split()
            try:
                this_board = [int(i) for i in this_board]
                self.known_boards.append(this_board)
            except ValueError:
                print '[WARN]: a board in', self.boards_file, 'had a non-integer value:', board

        self.known_boards = sorted(self.known_boards, key = self.num_free, reverse = True)
        print self.known_boards

    def num_free(self, board):
        num_free = 0

        for pos in board:
            if pos == EMPTY: 
                num_free += 1

        return num_free

class PerfectPlayer:
    def __init__(self, player):
        self.player = player

    # normally the move will be made using a minimax with alpha beta pruning. The exception is
    # the first move because this is where minimax is by far the slowest but the easiest to make a decision about
    def make_move(self, board):
        num_moves = 0;
        corner_move = False

        corners = ((0,0), (0,SIZE-1), (SIZE-1,0), (SIZE-1,SIZE-1))
        center = SIZE**2/2

        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] != EMPTY:
                    num_moves += 1
                    if (i,j) in corners: corner_move = True

        if not num_moves: return 0
        if num_moves == 1 and corner_move: return center

        move = self.minimax(self.player, board, 0, -100, 100)
        return move

    # find ideal move using minimax algorithm with alpha beta pruning.
    def minimax(self, player, board, depth, alpha, beta):
        if Game.game_over(board): return self.score(board, depth)

        # all empty positions where a move can be made
        moves = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == EMPTY]

        best_score = alpha if player == self.player else beta

        # try each move and see how well it does
        for move in moves:
            this_board = deepcopy(board)

            # make the move
            i, j = move
            this_board[i][j] = player

            # maximizing player
            if player == self.player:
                score = self.minimax(-1*player, this_board, depth+1, best_score, beta)
                
                if score > best_score:
                    best_score = score
                    best_move = j*SIZE + i

                if beta <= best_score: break
            # minimizing player
            else:
                score = self.minimax(-1*player, this_board, depth+1, alpha, best_score)
                
                if score < best_score:
                    best_score = min(best_score, score)
                    best_move = j*SIZE + i

                if best_score <= alpha: break

        return best_score if depth else best_move

    # how to score a result. 10 is max value because we can have up to 9 recursion depths
    # want to win in shortest amount of time or tie in greatest amount of time (prolong game)
    def score(self, board, depth):
        winner = Game.winner(board)

        if winner == self.player:   # I win
            return (10)
        if winner == (-1*self.player):  # I lose
            return (-10)

        return 0    # ties

# LP = LearningPlayer()

# board = [ 
#             [1, 0 , 1],
#             [-1, 0, 0],
#             [0, 0, 0]
#         ]

# print LP.ideal_move(board, -1)

# LP.train_move(-1, [[0,0,0],[0,1,0],[-1,0,0]], 7)
# LP.train_move(1, [[1,0,0],[-1,1,0],[-1,0,0]], 2)

# for i in range(1000):
#     LP.train_move(-1, [[0,0,0],[0,1,0],[-1,0,0]], 7)
#     LP.train_move(1, [[1,0,0],[-1,1,0],[-1,0,0]], 2)