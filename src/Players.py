from NeuralNetwork import NeuralNetwork
from Constants import SIZE, X, O, EMPTY
from GameState import Game
from Memories import Memories
from copy import deepcopy

class LearningPlayer:
    def __init__(self, player):
        self.player = player

        self.new_neural_net()

        self.memories = Memories()

    # make a new neural net. The number of hidden nodes, learning rate and momentum
    # were found experimentally.
    def new_neural_net(self):
        input_size = output_size = SIZE**2

        self.net = NeuralNetwork([input_size, 20, output_size])
        self.net.set_learning_rate(.002)
        self.net.set_momentum(.8)

    def get_player(self):
        return self.player

    def set_player(self, player):
        self.player = player

    # get the move from the neural network
    def make_move(self, board, learning = False):
        # flatten the board from a grid to 1D for the neural network
        if learning:
            inputs = Game.flatten(board)
        else:
            inputs = Game.flatten(board, self.player)

        self.memories.observe(inputs)

        # get the neural networks movs
        self.net.set_input(inputs)
        self.net.forward_propagate()
        output = self.net.get_output()

        # if we are learning, we want to take the neural networks top choice,
        # but if we are in a game, it needs to pick a valid move
        while True:
            move = output.index(max(output))    # highest rated move by NN
            # Convert to x, y
            y = move/SIZE
            x = move%SIZE
        
            if learning: return move

            if board[x][y] == EMPTY:
                return move

            else:
                output[move] = -1


    def learn_all_known_boards(self):
        self.passed_moves = self.failed_moves = 0

        # solve from the reference frame of the X player
        perfect_player = PerfectPlayer(X)

        for board in self.memories.get_memories():
            # build a grid out of a flattened board
            grid_board = Game.unflatten(board)

            # don't recompute move, if it's already be calculated
            if self.memories.remember_move(board) >= 0:
                correct_move = self.memories.remember_move(board)
            # get the move from the perfect player and store it in memory
            else:
                correct_move = perfect_player.make_move(grid_board)
                self.memories.learn_move(board, correct_move)

            self.learn_move(grid_board, correct_move) # learn the move

    # have the neural network 'learn' a move
    def learn_move(self, board, correct_move):
        my_move = self.make_move(board, True)    # the neural nets move

        if my_move == correct_move: self.passed_moves += 1 # it got it right!

        else:
            self.failed_moves += 1

            # excpeted the right move to be 100% likely and the others to be 0% likely
            expected_output = [0 for i in range(SIZE) for j in range(SIZE)]
            expected_output[correct_move] = 1
            self.net.back_propagate(expected_output)    # this is where the 'learning' is done

    def forget(self):
        self.new_neural_net()

class PerfectPlayer:
    def __init__(self, player):
        self.player = player

    def set_player(self, player):
        self.player = player

    def get_player(self):
        return self.player

    # the move is decided using a minimax algorithm with alpha beta pruning
    def make_move(self, board):
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

    # how to score a result
    def score(self, board, depth):
        winner = Game.winner(board)

        if winner == self.player:   # I win
            return 10
        if winner == (-1*self.player):  # I lose
            return -10

        return 0    # tie