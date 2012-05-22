# TODO: there are tidier ways to implement getter/setters here (more pythonic)

class Player(object):
    def __init__(self, colour):
        self.engine = None
        self.logger = None
        self.colour = colour
		
    def set_engine(self, engine):
        self.engine = engine

    def set_logger(self, logger):
        self.logger = logger

    def set_colour(self, colour):
        self.colour = colour
		
    def genmove(self):
        ''' generate a move, return coordinates (tuple) or where i want to move.'''
        ''' coordinates are 1-based.'''
        return None 

    def play(self, pos, colour):
        ''' notify me that a certain player (potentially myself) has played a particular move. '''
        ''' pos is a tuple of coordinates - one based. colour: 1 is black, 2 is white. '''
        pass

    def reset(self):
        ''' notify me that game/board/engine/etc. has been reset, so i can reset any state i kept. '''
        pass
