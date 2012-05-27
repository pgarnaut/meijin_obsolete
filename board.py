'''

Holds all the necessary state, including captures etc.

* black value is 1, white value is 2
* coordinates are one-based, and are generally of the form (col, row), to match standard go notation

* so far everything in this file is very minimal, no calculations/ validity checking / etc. - this is desired

'''

import sys
import gtp
import itertools

class Grid(object):
    def __init__(self, size = 9, oneBased = True):
        # create 2D array of Squares
        self.size = size
        self._elements = []
        for x in range(0,size * size):
            self._elements.append(Square()) 
        self.myOneBased = oneBased
        
    @property
    def raw(self):
        return self._elements
    
    def setOneBased(self, yes=True):
        self.myOneBased = yes
        
    @property
    def oneBased(self):
        return self.myOneBased
    
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

class Square():
    def __init__(self):
        self._colour = 3 
        self.visited = False
        self.l = 0 # liberty count 
        self.i = 0 # influence value
    
    def set_colour(self, colour):
        self._colour = colour

    def get_colour(self):
        return self._colour

    # alternative to the @property decorator syntax ...
    colour = property(get_colour, set_colour)

    def dup(self):
        tmp = Square()
        tmp._colour = self._colour
        tmp._visited = self.visited
        tmp.l = self.l
        tmp.i = self.i
        return tmp

    def __str__(self):
        if self._colour == 1:
            return 'x'
        elif self._colour == 2:
            return 'o'
        elif self._colour == 3:
            return '.' 
        else:
            raise Exception("Square element with bogus value: "+str(self._colour))

    property(get_colour, set_colour)

class Board():
    '''
    classdocs
    '''

    def __init__(self, size):
        '''
        Constructor
        '''
        # 3 is empty, 0 is black, 1 is white
        self._size = size
        self._grid = Grid(self._size)

    def __str__(self):
        ''' string representation of the board. '''
        # those pretty little markers at certain points ... use permutations with replacement
        markers = {9 : [k for k in itertools.product([3,7], repeat=2)], 
                   13: [k for k in itertools.product([4,10], repeat=2)], 
                   19: [k for k in itertools.product([4,10,16], repeat=2)]}

        s = "   "
        # print coloumn headers
        for col in range(1, self._size + 1, 1):
            if ord('a') + col - 1 >= ord('i'):
                col += 1 # skip the letter I
            s += ' ' + chr(ord('a') +  col -1)  
                
        s += "\n"
       
        # print each row, preceeded by row number
        for row in range(1, self._size + 1, 1):
            if self.size > 9 and row < 10:
                s += ' ' # alignment for 2 digits
            s += (' ' + str(row)) # print row header at start
            for col in range(1, self._size + 1, 1):
                # print markers here
                if self._size in markers.keys() and \
                    (col,row) in markers[self.size] and\
                    self._grid[col,row].colour == 3: 
                    s += ' +'
                else:
                    s += ' ' + str(self._grid[col,row]) 
                    
            s += (' ' + str(row)) # print row header at end
            s += "\n"

        # print coloumn headers again (underneath)
        s += "   "
        for col in range(1, self._size + 1, 1):
            if ord('a') + col - 1 >= ord('i'):
                col += 1 # skip the letter I
            s += ' ' + chr(ord('a') +  col -1)
        s += "\n"

        return s

    @property
    def size(self):
        return self._grid.size
        
    def reset(self):
        ''' empty everything on the board.'''
        self._grid = Grid(self.size)
    
    def resize(self, size):
        ''' empty the board (maybe) and resize it. '''
        self._grid = Grid(size)
        self._size = size
        
    
    def unvisit(self):
        ''' reset all the ._visited fields.'''
        for col in range(1,self.size + 1):
            for row in range(1,self.size + 1):
                self._grid[col,row].visited = False
    
    def set_stone(self, position, colour):
        ''' set board at position (tuple) to have colour (int). '''
        self._grid[position].colour = colour

    def remove_stones(self, positions):
        ''' just set a bunch of positions to empty.'''
        for p in positions:
            self._grid[p].colour = 3 # merely set the squares to empty
    
    
    def dup(self):
        tmp = Board(self.size)
        for col in range(1,self.size + 1):
            for row in range(1,self.size + 1):
                tmp._grid[col,row] = self._grid[col,row].dup()
        return tmp
    
    def __getitem__(self, idx):
        return self._grid[idx]
    
#    def __setitem__(self, idx, val):
#        self._grid[idx] = val
