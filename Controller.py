from GUI import Display
from GameState import Game
from Constants import EMPTY, X, O, SIZE
from Players import LearningPlayer, PerfectPlayer

class Controller:
    def __init__(self):
        self.curr_player = X

        self.computer_player = LearningPlayer()
        self.perfect_player = PerfectPlayer(O)

        self.game = Game()
        
        self.gui = Display(self)
        self.gui.mainloop()

    def reset(self):
        self.curr_player = X
        self.game = Game()

    def make_move(self, x, y):
        if self.get_position(x,y) == EMPTY and self.game.set_position(self.curr_player, x, y):
            self.switch_player()

            winner = self.check_winner()

            if not winner:
                self.get_computer_move()

    def get_computer_move(self):
        move = self.perfect_player.make_move(self.game.board)
        # move = self.computer_player.make_move(self.curr_player, self.game.board)

        y = move/SIZE
        x = move%SIZE

        self.game.set_position(self.curr_player, x, y)
        self.gui.update_button(x, y)

        self.check_winner()

        self.switch_player()

    def learn(self):
        print '\n\nLearning\n\n'
        for i in range(5000):
            self.computer_player.train_on_all_known_boards()    # TODO set who is which player
            print 'Pass', i, 'correct_moves:', self.computer_player.passed_moves, 'incorrect moves:', self.computer_player.failed_moves
            if not self.computer_player.failed_moves: break

    def get_position(self, x, y):
        return self.game.get_position(x, y)

    def check_winner(self):
        winner = self.game.winner1()

        if winner:
            self.gui.game_over(winner)
            return True
        elif self.game.board_full1():
            self.gui.game_over(None)
            return True

        return False

    def switch_player(self):
        if self.curr_player == X:
            self.curr_player = O
        else:
            self.curr_player = X

if __name__ == '__main__':
    a = Controller()