Non-technical how to play:

Double-click on the Tic-Tac-Toe file to play.

Simply press the buttons of the board to make moves. After every game press Learn and watch the computer get smarter! Press Forget if you want to be able to beat it again.

You will notice that the game will open as well as a window called Terminal. Print outs regarding the learning process will be in the Terminal window. To exit the program close the game and quit the Terminal.

Score:
+2 points for a win
-1 point for a tie
-2 points for a loss



Slightly more technical:

This program uses a Feed Forward, Back Propagation Neural Network to learn how to play Tic Tac Toe. What makes this program different from other similar projects is that the machine only learns what it has been exposed to. At first, the network will just choose a random move based on the random connections of the nerual network. As you play, it stores each board combination that it encounters. When you press learn, the neural network will learn what an ideal minimax player would have done for each of the encountered boards. The forget button causes the neural network connections to be randomized, however, all of the encountered boards are still in memory so the next time learn is pressed, all of the boards will be relearned. To truely wipe all of the boards out of memory, you would have to clear out the src/known_boards.txt file.

All source code can be found in the src directory.