'''
Implements the GTP commands and also does the thinking.


'''
import gtp
import random
import sys
import monkey
from gtp import Logger
from utils import Utils
move_list = [] # cant even remember what iwas doing with this ...

class Engine(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.logger = None
        self.validity_test_id = 0
        self.validity_testing = False
        self.validity_test_last_result = 0
        self.validity_test_results = []
        self.temp_test_move_list = [(1,1), (2,2), (5,5), (9,9)]
        self.board_size = 9
        
   
    # ---------------------------
    # gtp interface functions
    # ---------------------------
    
    def boardsize(self, size):
        self.board.resize(int(size))

    def clear_board(self):
        self.board.reset()
        # TODO: reset other state stuff here if necessary

    def komi(self, value):
        pass

    def play(self, color, vertex):
        vertex = Utils.parse_vertex(vertex, self.getBoardSize()) # may be None
        color = 1 if color[0].lower() == 'b' else 2
        #if self.board[vertex] != 3: # must be empty square
        #    raise Exception('illegal move')
        captures = []
        
        # check the validity of the move and determine any resulting captures
        self.validity_test_last_result = Utils.check_move(self.board, vertex, color, captures)
        
        if not self.validity_test_last_result:
            raise Exception("you played an invalid move")
        
        # place the stone
        self.board.set_stone(vertex, color)
        
        # apply any resulting captures 
        self.board.remove_stones(captures)
        
        #    def undo(self):
        #    pass

    def genmove(self, colour):
        ''' Ask the appropriate player to generate a move. '''
        colour = Utils.parse_colour(colour)
        
        # generate move
        move = self.players[colour - 1].genmove()
        captures = [] 

        # player should not generate an invalid move ...
        if not Utils.check_move(self.board, move, colour, captures):
            raise Exception("player " +Utils.make_colour(colour) + " generated an invalid move")
            
        # apply move to the board TODO: keep score here ...
        self.board.set_stone(move, colour)
        self.board.remove_stones(captures)

        # make GTP result string ...
        return Utils.make_vertex(move[0], move[1], self.board.size)
    
    def quit(self):
        sys.exit(0)
    
    def showboard(self):
        self.logger.logConsole(str(self.board))
    
    def name(self):
        return "meijin"
        
    # ---------------------------
    # non gtp interface functions
    # ---------------------------
    def getBoardSize(self): # TODO:
        return self.board.size
    
    def set_logger(self, logger):
        self.logger = logger
        Utils.set_logger(logger)
        
    def set_board(self, board):
        self.board = board
    
    def get_board(self):
        ''' get the current board.'''
        '''inefficient but the dup here prevents accidental modification of my board instnace.'''
        return self.board.dup()

    def set_players(self, p1, p2):
        self.players = [p1, p2]
        
    def start_validity_test(self, id):
        self.validity_test_id = int(id)
        self.validity_testing = True
        self.validity_test_last_result = 0
    
    def check_validity_test(self, result):
        if self.validity_test_last_result == int(result):
            self.validity_test_results.append((self.validity_test_id, True))
        else:
            self.validity_test_results.append((self.validity_test_id, False))
    
    def print_validity_test_results(self):
        for id,result in self.validity_test_results:
            self.logger.logTestout("["+ str(id)+"] ")
            if result:
                self.logger.logTestout("PASS\n")
            else:
                self.logger.logTestout("FAIL\n")
    
    def set_testout_only(self):
        self.logger.set_testout_only()
