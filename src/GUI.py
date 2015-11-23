from Tkinter import Tk, Button, Label
from tkFont import Font

from Constants import EMPTY, X, O, SIZE, STRINGS

class Display:
    def __init__(self, controller):
        # initialize the GUI
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Helvetica", size=32)

        self.game_controller = controller   # interface to the game

        self.winner = None  # who has won the game

        # make the board
        self.buttons = [[None for i in range(SIZE)] for j in range(SIZE)]
        for x in range(SIZE):
            for y in range(SIZE):
                handler = lambda x=x, y=y: self.move(x,y)   # each button corresponds to making a move in that square
                button = Button(self.app, command=handler, font=self.font, width=1, height=1)
                button.grid(row=y, column=x+SIZE)
                self.buttons[x][y] = button
        
        # button to reset the board
        handler = lambda: self.reset()
        button = Button(self.app, text='reset', command=handler, height=4)
        button.grid(row=SIZE+1, column=SIZE, columnspan=1, sticky="WE")

        # button that makes the machine learn
        handler = lambda: self.learn()
        button = Button(self.app, text='learn', command=handler, height=4)
        button.grid(row=SIZE+1, column=SIZE+SIZE/2, columnspan=1, sticky="WE")

        # button that causes the machine to forget how to play
        handler = lambda: self.forget()
        button = Button(self.app, text='forget', command=handler, height=4)
        button.grid(row=SIZE+1, column=2*SIZE-1, columnspan=1, sticky="WE")

        self.update()

        # the score labels
        score = Label(self.app, text='SCORE:', font=self.font)
        score.grid(row=0, column=0, columnspan=SIZE, sticky="WE")

        self.score = Label(self.app, text='0', font=self.font)
        self.score.grid(row=1, column=1, columnspan=1, sticky="WE")

    def mainloop(self):
        self.app.mainloop()

    def forget(self):
        self.game_controller.forget()

    def learn(self):
        self.game_controller.learn()
     
    def reset(self):
        # clear the winner textbox if there is one
        if self.winner != None:
            self.winner.destroy()
            self.winner = None

        # TODO this is for OSX
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
        # conver the board position value to a string
        text = STRINGS[self.game_controller.get_position(x, y)]
        self.buttons[x][y]['text'] = text
        # self.buttons[x][y]['disabledforeground'] = 'black'

        # TODO commented out for macs
        # disable a button if it is a position that has already been taken
        # if text == STRINGS[EMPTY]:
        #     self.buttons[x][y]['state'] = 'normal'
        # else:
        #     self.buttons[x][y]['state'] = 'disabled'        

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
            self.winner = Label(self.app, text="TIE", font=self.font)
            score -= 1
        else:
            text = 'Player', winner_str, 'Wins!'
            self.winner = Label(self.app, text=text, font=self.font)

        self.winner.grid(row=1, column=3*SIZE, columnspan=SIZE, sticky="WE")

        # display the score
        self.score['text'] = str(score)