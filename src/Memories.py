from Constants import EMPTY

class Memories:
    def __init__(self):
        self.file_name = '/home/dnav/Desktop/TicTacToe/src/known_boards.txt'

        # how we'll store memories. Key is a board, value is the associate move
        self.memories = {}

        self.remember()     # load memories from file

    # just the boards
    def get_memories(self):
        return sorted(self.memories.keys(), key = self.num_free)

    # see how many empty positions there are on a board. For sorting purposes
    def num_free(self, board):
        num_free = 0

        for pos in board:
            if pos == EMPTY: 
                num_free += 1

        return num_free

    def learn_move(self, board, move):
        self.memories[board] = move

    # get the move associated with a board
    def remember_move(self, board):
        if not board in self.get_memories(): return -1

        return self.memories[tuple(board)]

    # add the memory and write it out to the file. -1 means no known move yet
    def make_new_memory(self, board, from_long_term_mem=False):
        self.memories[tuple(board)] = -1

        if not from_long_term_mem: self.long_term_potentiation(board)

    # if there is a memory of this board do nothing, otherwise add it to memory
    def observe(self, board, from_long_term_mem=False):
        if tuple(board) in self.get_memories(): return

        else: self.make_new_memory(board, from_long_term_mem)

    # load all of the memory from the file
    def remember(self):
        try:
            boards = open(self.file_name)
        except IOError:
            print '\n\n[ERR]: could not find memory in known_boards.txt\n\n'

        for board in boards:
            this_board = board.split()
            try:
                this_board = [int(i) for i in this_board]
                self.observe(this_board, True)
            except ValueError:
                print '[WARN]: a board in', self.file_name, 'had a non-integer value:', board

    # put it in long term memory, i.e. right to file
    def long_term_potentiation(self, board):
        with open(self.file_name, "a") as boards:
            boards.write('\n')
            boards.write(' '.join(str(i) for i in board))