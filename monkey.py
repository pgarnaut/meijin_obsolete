'''

'''
import board
import engine
import sys
from player import Player
from utils import Utils

import itertools, math, random

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
        
        # TODO: not sure if there is a more succinct way to do this:
        # yank each coordinate within the blob
        for sq in dims:
            blob = []
            top_left = sq[0]
            bottom_right = sq[1]
            for col in range(top_left[0], bottom_right[0] + 1):
                for row in range(top_left[1], bottom_right[1] + 1):
                    blob.append((col,row))
            yield blob

    def influence_in_blob(self, blob):
        ''' return total influence value over a blob of coordinates. '''
        inf = 0
        for coord in blob:
            inf += self._engine.board[coord].i
        
        return inf

    def empty_quads(self, inf):
        pass
        

    def genmove(self):
        b = self.engine.board
        size = b.size
        
        # check the corner blobs
        for blob in self.corners(b, 3):
            influence = self.influence_in_blob(blob)
            dominator = (1 if influence > 0 else 2)
            
            # enemy dominates it
            if dominator != self._colour:
                for coord in blob:
                    if b[coord].colour == 3 and Utils.check_move(b, coord, self.colour, []):
                        return coord
               
            # no one owns it yet    
            elif influence == 0:
                random.shuffle(blob)
                blob.sort()
                return blob[int(len(blob)/2)]
            
            # I dominate it ...
            else:   
                pass
        
        # nothing to do at the corners ...
        
        possible = [k for k in itertools.product(range(1, size+1), repeat=2) if b[k].colour == 3]
        random.shuffle(possible)
                    
        last_valid = None
        for v in possible:
            if Utils.check_move(b, v, self.colour, []):   
                last_valid = v  
                if random.choice(range(10)) == 1:
                    break
            
        return last_valid
                
        