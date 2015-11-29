from Tkinter import Tk, Button, Label, OptionMenu, StringVar
from tkFont import Font

from Constants import EMPTY, X, O, SIZE, STRINGS

class Display:
    def __init__(self, controller):
        # initialize the GUI
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.game_controller = controller   # interface to the game

        self.winner = None  # who has won the game

        # make the board
        self.buttons = [[None for i in range(SIZE)] for j in range(SIZE)]
        for x in range(SIZE):
            for y in range(SIZE):
                handler = lambda x=x, y=y: self.move(x,y)   # each button corresponds to making a move in that square
                self.buttons[x][y] = self.make_button(text='', command=handler, row=y, column=x+SIZE, width=1)
        
        # button to reset the board
        self.make_button(text='New Game', command=lambda:self.reset(), row=SIZE+1, column=SIZE)
        # button that makes the machine learn
        self.make_button(text='Learn', command=lambda:self.learn(), row=SIZE+1, column=SIZE+SIZE/2)
        # button that causes the machine to forget how to play
        self.make_button(text='Forget', command=lambda:self.forget(), row=SIZE+1, column=2*SIZE-1)

        self.update()

        # the score labels
        score = Label(self.app, text=' SCORE:', font=Font(family="Courier", weight='bold', size=32))
        score.grid(row=0, column=0, columnspan=SIZE)
        self.score = Label(self.app, text='0', font=Font(family="Courier", weight='bold', size=32))
        self.score.grid(row=1, column=1)

        # choose if you are X or O. X always goes first
        self.player_choice = StringVar()    # how to keep track of the option
        which_player = OptionMenu(self.app, self.player_choice, *(STRINGS[X], STRINGS[O])) # options are X and O
        which_player.grid(row=SIZE+2, column=SIZE+2)
        which_player.config(font=Font(family='Courier'))
        self.player_choice.set('X')
        self.player_choice.trace('w', self.choose_player)

        # choose between playing against a Perfect player or Learning player
        self.comp_type = StringVar()    # how to keep track of the option
        comp_type = OptionMenu(self.app, self.comp_type, *('Learning', 'Perfect'))
        comp_type.grid(row=SIZE+2, column=SIZE)
        comp_type.config(width=11, font=Font(family='Courier'))
        self.comp_type.set('Learning')
        self.comp_type.trace('w', self.choose_comp_type)

    def mainloop(self):
        self.app.mainloop()

    # make a new button
    def make_button(self, text, command, row, column, width=None):
        if width: button = Button(self.app, text=text, command=command, width=width, font=Font(family="Courier"))
        else: button = Button(self.app, text=text, command=command, font=Font(family="Courier"))
        button.grid(row=row, column=column, columnspan=1)
        return button

    # choose if you will be X or O player
    def choose_player(self, *args):
        if hasattr(self, 'prev_player'):    # only returns false first time
            if self.player_choice.get() != self.prev_player:    # only do something if the choice has changed
                self.prev_player = self.player_choice.get()     # get the choice

                self.game_controller.set_player(self.prev_player)   # set the player
                self.reset()    # new game. Can't switch player mid game

        else:
            self.prev_player = self.player_choice.get() # get the choice

            if self.prev_player == STRINGS[O]:  # this is the first time so only has changed if it switched to O
                self.game_controller.set_player(self.prev_player)
                self.reset()

    # choose between playing against a perfect player or learning player
    def choose_comp_type(self, *args):
        if hasattr(self, 'prev_comp_type'):     # only returns falls first time
            if self.comp_type.get() != self.prev_comp_type:     # only do something if the choice has changed
                self.prev_comp_type = self.comp_type.get()      # get the choice

                self.game_controller.set_comp_type(self.prev_comp_type)     # set the type

        else:
            self.prev_comp_type = self.comp_type.get()  # get the choice

            if self.prev_comp_type == 'Perfect':    # this is the first time so only has changed if it switched to perfect
                self.game_controller.set_comp_type(self.prev_comp_type)

    def forget(self):
        self.game_controller.forget()

    def learn(self):
        self.game_controller.learn()
     
    def reset(self):
        # clear the winner textbox if there is one
        if self.winner != None:
            self.winner.destroy()
            self.winner = None

        # reenable the board
        for x in range(SIZE):
            for y in range(SIZE):
                self.buttons[x][y]['state'] = 'normal'

        self.game_controller.reset()

        self.update()
    
    # make a move and update the display
    def move(self,x,y):
        self.game_controller.make_move(x,y)

        self.update_button(x, y)
        self.app.config(cursor="")

    # update all the buttons to reflect the game state
    def update(self):
        for x in range(SIZE):
            for y in range(SIZE):
                self.update_button(x, y)

    # update a single button
    def update_button(self, x, y):
        # convert the board position value to a string
        text = STRINGS[self.game_controller.get_position(x, y)]
        self.buttons[x][y]['text'] = text

    # game has ended. disable the board and display the results
    def game_over(self, winner):
        # disable the board
        for x in range(SIZE):
            for y in range(SIZE):
                self.buttons[x][y]['state'] = 'disabled'

        # update the score
        score = int(self.score['text'])

        # display the result of the game
        if winner == X:
            winner_str = '1'
            score += 2
        elif winner == O:
            winner_str = '2'
            score -= 2

        if winner == None:
            self.winner = Label(self.app, text="TIE", font=Font(family="Courier", weight='bold', size=32))
            score -= 1
        else:
            text = 'Player', winner_str, 'Wins!'
            self.winner = Label(self.app, text=text, font=Font(family="Courier", weight='bold', size=32))

        self.winner.grid(row=1, column=3*SIZE, columnspan=SIZE, sticky="WE")

        # display the score
        self.score['text'] = str(score)