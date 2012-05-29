# it's quite likely that these libraries dont exist on many peoples platforms
# there's probably a better way to avoid rewriting function declarations here ..
try:
    import numpy
    import matplotlib.pyplot as plt
    from pylab import *
    import time
    
    class Visualise(object):
        '''
        classdocs
        '''
    
        def __init__(self, logger = None):
            '''
            Constructor
            '''
            self._logger = logger
        
        def visualise_influence(self, board, wait=0):
            vals = numpy.zeros( (19,19), dtype='float64')
            for row in range(1, board.size + 1):
                for col in range(1, board.size + 1):
                    vals[col-1, row-1] = board[col,row].i
            
            plt.close()
                    
            f = plt.figure()
            plt.subplots_adjust(hspace=0.5)
            ax = f.add_subplot(121)
            ax.imshow(vals, interpolation='quadric')
            f.canvas.draw()
            
            plt.show()
            
# couldn't load libraries for visualisation ...
except Exception:
    class Visualise(object):
        def __init__(self, logger = None):
            self._logger = logger
        def visualise_influence(self, board, wait=0):
            if self._logger is not None:
                self._logger.log_comment("#warning: visualise_influence: failed to load visualisation libraries")
        