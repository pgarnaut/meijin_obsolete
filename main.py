'''
Entry point.





NOTES:
throughout code, black = 1, white = 2, empty = 3
all coordinates are 1-based
'''

import sys
from engine import Engine
from player import Player
from monkey import Monkey, Human
from gtp import GTP, Logger
from board import Board

''' 
TODO: need options:
--human : gtp like mode
--engine : act like an engine for a gui 
--test : read session file from disk
'''
usage_str = """
python main.py <options>
--human
--test <filename>
--engine
"""

def usage():
    w = sys.stderr.write(usage_str)
    sys.exit(1)

if __name__ == '__main__':
    # create logger - all logging done through this:
    logger = Logger()
    
    in_file = None
    do_human = False

    args = sys.argv[1:]
    if len(args) < 1:
        usage()
    if args[0] == "--human":
        do_human = True 
    elif args[0] == "--test":
        in_file = (open(args[1], "r") if len(args) >= 2 else usage())
    elif args[0] == "--engine":
        in_file = sys.stdin
    else:
        usage()

        
    # create players
    p1 = (Human(1) if do_human else Player(1))
    p2 = Monkey(2) # AI - can do play_move() and gen_move()
    
    # create engine
    engine = Engine()
    
    # create board of default size 9
    board = Board(9)
    
    # create gtp_parser
    gtp = GTP(in_file)
    
    # attach everything
    engine.set_board(board)
    engine.set_players(p1, p2)
    engine.set_logger(logger)
    p1.set_engine(engine)
    p2.set_engine(engine)
    gtp.set_engine(engine)
    gtp.set_logger(logger)
        
    # start reading commands from in_file 
    if not do_human:
        gtp.run()
    else:
        players = ["black", "white"]
        p = 0
        while True:
           engine.showboard()
           engine.genmove(players[p])
           p = (p + 1) % 2
