'''
Implements the GTP commands and stores the state of the game.
'''
import sys
from utils import Utils
from visualise import Visualise

class Move(object):
    def __init__(self, p, c, caps):
        self.p = p # position
        self.c = c # colour
        self.caps = caps # captures, list of coordinate tuples

class Engine(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._logger = None
        self._board = None
        self._players = []
        
        self.validity_test_id = 0
        self.validity_testing = False
        self.validity_test_last_result = 0
        self.validity_test_results = []
        
        # number of captured stones (not the positions of captures)
        self._captures = [0, 0] 
        # list of Move objects
        self._moves = []
        # visualisation utilities
        self._vis = None
   
    # ---------------------------
    # gtp interface functions
    # ---------------------------
    
    def boardsize(self, size):
        ''' set the board size. '''
        self._board.resize(int(size))

    def clear_board(self):
        self._board.reset()
        # TODO: reset other state stuff here if necessary

    def komi(self, value):
        pass

    def play(self, color, vertex):
        vertex = Utils.parse_vertex(vertex, self._board.size) # may be None
        color = 1 if color[0].lower() == 'b' else 2
        self.apply_move(vertex, color)

    def genmove(self, colour):
        ''' Ask the appropriate player to generate a move. '''
        colour = Utils.parse_colour(colour)
        
        # generate move
        move = self._players[colour - 1].genmove()
        
        self.apply_move(move, colour)
        # make GTP result string ...
        return Utils.make_vertex(move[0], move[1], self._board.size)
    
    def apply_move(self, vertex, colour):
        ''' apply move to engine (and players). '''
        captures = []
        
        self.validity_test_last_result = Utils.valid_coord(vertex, self.board.size)
        
        # check the validity of the move and determine any resulting captures
        self.validity_test_last_result = \
                        self.validity_test_last_result and \
                        Utils.check_move(self._board, vertex, colour, captures)
        
        if not self.validity_test_last_result:
            raise Exception("you played an invalid move: " + str(colour) + " " + str(vertex))
        
        self._moves.append(Move(vertex, colour, captures))
        
        # place the stone
        self._board.set_stone(vertex, colour)
        
        # apply any resulting captures 
        self._board.remove_stones(captures)
        
        # apply influence values to board squares 
        Utils.calc_influence(self._board)
        
        self._players[0].play(vertex, colour)
        self._players[1].play(vertex, colour)
 
    
    def show_influence(self):
        return Utils.show_influence(self._board)
    
    def vis_influence(self):
        if self._vis is None:
            self._vis = Visualise()
        self._vis.visualise_influence(self._board, 0)
    
    def quit(self):
        sys.exit(0)
    
    def showboard(self):
        ''' print board to stdout. '''
        self._logger.log_console(str(self._board))
    
    def name(self):
        return "meijin"
        
    # ---------------------------
    # non gtp interface functions
    # ---------------------------

    def set_logger(self, logger):
        self._logger = logger
        Utils.set_logger(logger)
    
    def get_logger(self):
        return self._logger
    
    logger = property(get_logger, set_logger)
        
    def set_board(self, board):
        self._board = board
    
    def get_board(self):
        ''' get a clone of the current board.'''
        '''inefficient but the dup here prevents accidental modification of my board instance.'''
        return self._board #.dup()

    board = property(get_board, set_board)



    def set_players(self, p1, p2):
        self._players = [p1, p2]

    def undo(self):
        m = self._moves.pop()
        enemy_colour = (1 if m.c == 2 else 2)
        # remove the stone that was placed
        self._board.set_stone(m.p, 3)
        # replace captured stones
        for c in m.caps:
            self._board.set_stone(c, enemy_colour)
        # tell players to update their state
        for p in self._players:
            p.undo()
        
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
        for id_, result in self.validity_test_results:
            self._logger.logTestout("["+ str(id)+"] ")
            if result:
                self._logger.logTestout("PASS\n")
            else:
                self._logger.logTestout("FAIL\n")
    
    def set_testout_only(self):
        self._logger.set_testout_only()