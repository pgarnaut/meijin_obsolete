'''

'''
import board
import engine
import sys
from player import Player
from utils import Utils

import itertools, math

class Human(Player):
    def __init__(self, colour):
        super(Human, self).__init__(colour)

    def genmove(self):
        ''' politely ask user for a move. '''
        
        size = self.engine.board.size
        move = None
        while True:
            print("move:")
            move = sys.stdin.readline()
            if move.strip().lower() == "quit":
                sys.exit(0)
            
            move = Utils.parse_vertex(move, size)
            if Utils.valid_coord(move, size) and Utils.check_move(self.engine.board, move, self.colour, []):
                break
            else:
                print("invalid move")
        return move

class S(object):
    def __init__(self):
        self.c = 3 # colour (int)
        self.l = 0 # liberties (if applicable)
        self.i = 0 # influence (int)

class G(object):
    def __init__(self, size = 19):
        # create 2D array of Squares
        self.size = size
        self._elements = []
        for x in range(0,size * size):
            self._elements.append(S()) 
            
    def __getitem__(self, idx):
        ''' idx is tuple of (col, row).'''
        col = idx[0] - 1 # one based index
        row = idx[1] - 1 # one base index
        return self._elements[ col*self.size + row]
    
    def __setitem__(self, idx, val):
        ''' idx is tuple of (col, row).'''
        col = idx[0] - 1
        row = idx[1] - 1
        self._elements[ col*self.size + row ] = val



class Monkey(Player):
    '''
    classdocs
    '''

    def __init__(self, colour):
        super(Monkey, self).__init__(colour)

    def genmove(self):
        b = self.engine.board
        size = b.size
        empty = []
        for c in range(1, size+1):
            for r in range(1, size+1):
                if b[c,r].colour == 3:
                    empty.append((c,r))
                    
        for p in empty:
            if Utils.check_move(b, p, self.colour, []):
                return p   
                
