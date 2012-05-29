'''

'''
import board
import engine
import sys
from player import Player
from utils import Utils

import itertools, math, collections

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


class Blob(object):
    def __init__(self):
        self.coords = [] # list of coordinate tuples

class Monkey(Player):
    '''
    classdocs
    '''

    def __init__(self, colour):
        super(Monkey, self).__init__(colour)

    def corners(self, b, size=3):
        ''' return 4 element array, of arrays of the coordinates of the corners.'''
        ''' [ [(a,b), (c,d), ...], [], [], [] ]. '''
        s = b.size
        # top (top left corner), (bottom right corner) of each of the 4, 3x3 corner squares
        dims= [
               ((1,1), (size,size)),
               ((1,s-(size-1)), (size,s)), # quadrant 2 and 3 symetrical
               ((s-(size-1), 1), (s,size)),
               ((s-(size-1), s-(size-1)), (s, s))
        ]

        blobs = [ Blob(), Blob(), Blob(), Blob() ]
        
        # TODO: not sure if there is a more succinct way to do this:
        sq_idx = 0
        for sq in dims:
            top_left = sq[0]
            bottom_right = sq[1]
            for col in range(top_left[0], bottom_right[0] + 1):
                for row in range(top_left[1], bottom_right[1] + 1):
                    blobs[sq_idx].coords.append((col,row))
                    print((col,row))
            sq_idx += 1 # next quadrant
        return blobs 

    def quads_to_influence(self, blobs):
        ''' return 4 element tuple of influence delta in quadrants. '''
        inf = [[0,0], [0,0], [0,0], [0,0]]
        blob_idx = 0
        board = self._engine.board
        
        for blob in blobs:
            for sq in blob.coords:
                if board[sq].colour != 3:
                    inf[blob_idx][board[sq].colour - 1] += board[sq].i
            blob_idx += 1
        
        for blob in inf:
            print(blob)

        return inf

    def empty_quads(self, inf):
        pass

    def genmove(self):
        b = self.engine.board
        size = b.size
        empty = []
        
        blobs = self.corners(b)
        deltas = self.quads_to_influence(blobs)
        
        for c in range(1, size+1):
            for r in range(1, size+1):
                if b[c,r].colour == 3:
                    empty.append((c,r))
                    
        for p in empty:
            if Utils.check_move(b, p, self.colour, []):
                return p   
                
        