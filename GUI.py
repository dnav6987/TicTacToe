from Tkinter import Tk, Button, Label
from tkFont import Font

from Constants import EMPTY, X, O, SIZE, STRINGS

class Display:
    def __init__(self, controller):
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Helvetica", size=32)

        self.game_controller = controller

        self.buttons = [[None for i in range(SIZE)] for j in range(SIZE)]
        self.winner = None

        for x in range(SIZE):
            for y in range(SIZE):
                handler = lambda x=x, y=y: self.move(x,y)
                button = Button(self.app, command=handler, font=self.font, width=8, height=4)
                button.grid(row=y, column=x)
                self.buttons[x][y] = button
        
        handler = lambda: self.reset()
        button = Button(self.app, text='reset', command=handler, height=4)
        button.grid(row=SIZE+1, column=0, columnspan=2, sticky="WE")

        handler = lambda: self.learn()
        button = Button(self.app, text='learn', command=handler, height=4)
        button.grid(row=SIZE+1, column=2, columnspan=1, sticky="WE")

        self.update()

    def mainloop(self):
        self.app.mainloop()

    def learn(self):
        self.game_controller.learn()
     
    def reset(self):
        if self.winner != None:
            self.winner.destroy()
            self.winner = None

        self.game_controller.reset()

        self.update()
     
    def move(self,x,y):
        self.app.config(cursor="watch")
        self.app.update()
        
        self.game_controller.make_move(x,y)

        self.update_button(x, y)
        self.app.config(cursor="")

    def update(self):
        for x in range(SIZE):
            for y in range(SIZE):
                self.update_button(x, y)

    def update_button(self, x, y):
        text = STRINGS[self.game_controller.get_position(x, y)]
        self.buttons[x][y]['text'] = text
        self.buttons[x][y]['disabledforeground'] = 'black'

        if text == STRINGS[EMPTY]:
            self.buttons[x][y]['state'] = 'normal'
        else:
            self.buttons[x][y]['state'] = 'disabled'        

    def game_over(self, winner):
        for x in range(SIZE):
            for y in range(SIZE):
                self.buttons[x][y]['state'] = 'disabled'

        if winner == 1:
            winner_str = '1'
        else:
            winner_str = '2'

        if winner == None:
            self.winner = Label(self.app, text="TIE", font=self.font)
        else:
            text = 'Player', winner_str, 'Wins!'
            self.winner = Label(self.app, text=text, font=self.font)

        self.winner.grid(row=1, column=0, columnspan=SIZE, sticky="WE")