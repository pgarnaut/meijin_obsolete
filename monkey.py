'''

'''
import board
import engine
import sys
from player import Player
from utils import Utils

class Human(Player):
    def __init__(self, colour):
        super(Human, self).__init__(colour)

    def genmove(self):
        ''' politely ask user for a move. '''
        
        size = self.engine.get_board().get_size()
        move = None
        while True:
            print("move:")
            move = sys.stdin.readline()
            if move.strip().lower() == "quit":
                sys.exit(0)
            
            move = Utils.parse_vertex(move, size)
            if Utils.valid_coord(move, size) and Utils.check_move(self.engine.get_board(), move, self.colour, []):
                break
            else:
                print("invalid move")
        return move

class Monkey(Player):
    '''
    classdocs
    '''

    def __init__(self, colour):
        super(Monkey, self).__init__(colour)


    def genmove(self):
        b = self.engine.get_board()
        size = b.size
        empty = []
        for c in range(1, size+1):
            for r in range(1, size+1):
                if b[c,r].colour == 3:
                    empty.append((c,r))
        for p in empty:
            if Utils.check_move(b, p, self.colour, []):
                return p   
