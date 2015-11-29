from GUI import Display
from GameState import Game
from Constants import EMPTY, X, O, SIZE, STRINGS
from Players import LearningPlayer, PerfectPlayer

class Controller:
    def __init__(self):
        self.curr_player = X    # whose turn is it?

        # the computer players
        self.learning_player = LearningPlayer(O)
        self.perfect_player = PerfectPlayer(O)
        self.computer_player = self.learning_player

        self.game = Game()  # new game/board
        
        # run the gui
        self.gui = Display(self)
        self.gui.mainloop()

    # reset the game
    def reset(self):
        self.curr_player = X
        self.game = Game()

        if self.computer_player.get_player() == X: self.get_computer_move() # X goes first

    # Called by the GUI so this means a human moved. Update the game and get the computer's move
    def make_move(self, x, y):
        # check that the move is valid
        if self.get_position(x,y) == EMPTY and self.game.set_position(self.curr_player, x, y):
            self.switch_player()    # other players turn now

            winner = self.game_over()    # was there a winner?

            # game isn't over so get the computer player's move
            if not winner:
                self.get_computer_move()

    # get the move from the computer
    def get_computer_move(self):
        move = self.computer_player.make_move(self.game.board)  # the computer's move

        # convert from 1D to 2D
        y = move/SIZE
        x = move%SIZE

        self.game.set_position(self.curr_player, x, y) # update the game board
        self.gui.update_button(x, y)    # update the GUI

        self.game_over()     # check if the game is over

        self.switch_player()    # other players turn now

    # this is the fun stuff! Have the machine learn from the observed behavior
    def learn(self):
        print '\n\nLearning\n\n'

        # Ideally we want it to learn until it gets every move right, but at somepoint we have to stop learning
        for i in range(20000):
            self.learning_player.learn_all_known_boards()
            
            # see how many moves the machine got right and how many it got wrong
            print 'Pass', i, 'correct_moves:', self.learning_player.passed_moves, 'incorrect moves:', self.learning_player.failed_moves
            
            if not self.learning_player.failed_moves:   # got every move right!
                num_passes = i
                break

        print '\n\nIt took', i, 'iterations but I learned all of the moves!\n\n'

    def forget(self):
        self.learning_player.forget()

        print '\n\nI just forgot how to play\n\n'

    def get_position(self, x, y):
        return self.game.get_position(x, y)

    # has somebody won? if not, was there a tie?
    def game_over(self):
        winner = self.game.has_winner()

        if winner:  # somebody won
            self.gui.game_over(winner)
            return True
        elif self.game.is_full():   # board is full -> tie
            self.gui.game_over(None)
            return True

        return False    # game is not over

    # set what player the computer player is (X or O)
    def set_player(self, player):
        self.learning_player.set_player(-1*STRINGS[player])
        self.perfect_player.set_player(-1*STRINGS[player])

    # switch between whose turn it is
    def switch_player(self):
        if self.curr_player == X:
            self.curr_player = O
        else:
            self.curr_player = X

    # set the type of computer player (learning or perfect)
    def set_comp_type(self, comp_type):
        if comp_type == 'Perfect': self.computer_player = self.perfect_player
        else: self.computer_player = self.learning_player

if __name__ == '__main__':
    a = Controller()