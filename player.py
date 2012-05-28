from utils import Utils # for check_move()

# TODO: how do i implement setters properly without getters ...?

class Player(object):
    def __init__(self, colour):
        self._engine = None
        self._logger = None
        self._colour = colour

    def set_engine(self, engine):
        self._engine = engine
      
    def get_engine(self):
        return self._engine

    def set_logger(self, logger):
        self._logger = logger
        
    def get_logger(self):
        return self._logger

    def set_colour(self, colour):
        self._colour = colour

    def get_colour(self):
        return self._colour
        
    colour = property(get_colour, set_colour)
    logger = property(get_logger, set_logger)
    engine = property(get_engine, set_engine)    

    def genmove(self):
        ''' generate a move, return coordinates (tuple) or where i want to move.'''
        ''' coordinates are 1-based.'''
        # default behaviour: return first valid move
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
        return None 

    def play(self, pos, colour):
        ''' notify me that a certain player (potentially myself) has played a particular move. '''
        ''' pos is a tuple of coordinates - one based. colour: 1 is black, 2 is white. '''
        pass
    
    def undo(self):
        ''' notify me that the last move applied to engine has been undone.'''
        pass
    
    def reset(self):
        ''' notify me that game/board/engine/etc. has been reset, so i can reset any state i kept. '''
        pass
