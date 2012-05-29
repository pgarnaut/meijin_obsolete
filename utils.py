'''
    utils.py - tools/utilities for go engine
'''

import board
import engine
import sys
import itertools
import math

class Utils(object):
    '''
    classdocs
    '''
    logger = None
    

    @staticmethod
    def set_logger(dbg_logger):
        Utils.logger = dbg_logger

    @staticmethod    
    def valid_coord(c, size):
        ''' c is a tuple of [column, row], size is the board size. '''
        return True if (1 <= c[0] <= size and 1 <= c[1] <= size) else False

    @staticmethod    
    def parse_vertex(vertex, boardsize):
        ''' turn a string such as 'B19' into tuple of ints [2,19]. '''
        vertex = vertex.lower()
        if vertex == 'pass':
            return
        letter = vertex[0]
        number = vertex[1:]
        row = int(number)
        col = ord(letter) - ord('a') + 1
        if col >= 9:
            col-= 1 # GTP coordinates skip the letter 'I'
            
        return col, row
        
    @staticmethod    
    def make_vertex(col, row, boardsize):
        ''' turn col,row such as 2,19 into string "B19".'''
        if col >= 9:
            col += 1 # GTP coordinates skip the letter 'I'
        number = str(row)
        letter = chr(col + ord('a') - 1)
        return letter + number

    @staticmethod    
    def parse_colour(colour):
        ''' return int representation of colour string, "black" = 1, "white" = 2.'''
        colour = colour.lower()
        colour = colour[0]
        if colour == 'b':
            return 1
        else:
            return 2
        
    @staticmethod    
    def make_color(color):
        ''' turn int into string represnting colour.'''
        if color == 1:
            return 'black'
        else:
            return 'white'

    @staticmethod
    def captures(b, pos, adjacentEnemies):
        ''' 
            will set the visited flags on board, so be sure to reset after calling.
            
            adjacentEnemies is all the enemies adjacent to the piece played at pos, ie.
            you can assume b[pos].colour != colour of all positions in adjacentEnemies.
            
            TODO: potential inefficiencies having to univist the board for every enemy.
        '''
        #self.logger.logConsole("piece "+str(pos) +" has adjacent enemies: "+str(adjacentEnemies))
        dead = []
        for e in adjacentEnemies:
            friendlies = []
            if Utils.liberties(b, e, friendlies, [], []) == 0:
                dead = dead + friendlies
                dead.append(e)
            b.unvisit()
                
        #self.logger.logConsole("\thas " + str(len(dead)) + " captures")
        return dead
    
    @staticmethod
    def liberties(b, pos, friends, enemies, empties):
        ''' Find the friendly, enemy and empty squares adjacent to pos.
        Will set the visited flags on board, so be sure to reset after calling.
        Pos should of course not be an empty square.'''
        total = 0
        c = b[pos].colour
        neighbors = Utils.neighbors(b, pos)

        
        for n in neighbors:
            if not b[n].visited:
                b[n].visited = True
                if b[n].colour == 3:
                    total += 1
                    empties.append(n)
                elif b[n].colour == c:
                    friends.append(n)
                    total += Utils.liberties(b, n, friends, enemies, empties)
                else:
                    enemies.append(n)
                    
        return total
    
    @staticmethod
    def setLiberties(b):
        ''' assume no pending captures to be removed. O((n=81)^2)'''
        for col in range(1,b.size+1):
            for row in range(1,b.size+1):
                b[col,row].liberties = Utils.liberties(b, (col,row), [], [], [])
    
    # TODO: simplify this code further    
    @staticmethod
    def neighbors(b, pos):
        ''' get neighboring grid locations. '''
        # get neighbor grid coordinates
        col = pos[0]
        row = pos[1]
        neighbors = [ (col+1, row), (col-1, row), (col,row+1), (col, row-1)]
        neighbors = [(c,r) for c,r in neighbors if Utils.valid_coord((c,r), b.size)]

        return neighbors
    
    @staticmethod
    def neighborsToGroup(board, p):
        return []
 
    @staticmethod
    def check_move(board, vertex, color, captures=[]):
        ''' return True for valid, False for invalid, and fill out captures with any captured stones that will result.'''
        friends = []
        enemies = []
        # dont want to mung up the actual board maintianed by the engine
        board = board.dup() 

        if not Utils.valid_coord(vertex, board.size):
            return False
            
        # non empty square?
        if board[vertex].colour != 3:
            return False

        origColour = board[vertex].colour
        board[vertex].colour = color # be careful to undo this after checking it's validity
        
        board.unvisit()
        libs = Utils.liberties(board, vertex, friends, enemies, [])
        board.unvisit()
        captures.extend(Utils.captures(board, vertex, enemies))
        board.unvisit()
        
        
        # undo changes
        board[vertex].colour = int(origColour)
        
        if libs > 0 or len(captures) > 0:
            return True
        else:
            return False
          
    @staticmethod  
    def show_influence(g):
        for row in range(1, g.size + 1):
            for col in range(1, g.size + 1):
                Utils.logger.log_console(str(g[col,row].i) + " ")
            sys.stdout.write("\n")
            
    @staticmethod
    def influence_propogation(v):
        return math.floor(60 / (1 + v[0]**2 + v[1]**2))
  
    @staticmethod  
    def calc_influence(b):
        ''' Will overwrite existing influence values in board. '''
        # TODO: implement an "update_influence" function - will be more efficient
        
        # reset influence
        for row in range(b.size):
            for col in range(b.size):
                b[col,row].i = 0
        
        # the directions/distances and strength of propagation        
        mat = dict()
        for k in itertools.product(range(-3, 3), repeat=2):
            mat[k] = Utils.influence_propogation(k)
        
        # foreach square in board
        for row in range(1, b.size + 1):
            for col in range(1, b.size + 1):
                modifier =  1
                if b[col,row].colour == 2:
                    modifier = -1
                elif b[col,row].colour == 3: 
                    modifier = 0
                
                # foreach square we apply influence to from here ...
                for dP in mat.keys():
                    p = (col + dP[0], row + dP[1])
                    if Utils.valid_coord(p, b.size):   
                        b[p].i += modifier * mat[dP]
    
