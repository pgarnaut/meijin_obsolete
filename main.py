#!/usr/bin/python
'''
Entry point - creates players, board, engine and gtp parser.


NOTES:
throughout code, black = 1, white = 2, empty = 3
all coordinates are 1-based, where coordinates = (column, row) 

TODO: when run in --engine mode, set both players to be the AI player, that way any
genmove <colour> command will behave as expected.
'''
import sys
from engine import Engine
from player import Player
from monkey import Monkey, Human
from gtp import GTP, Logger
from board import Board


usage_str = """
python main.py <options>
--human
--test <filename>
--engine
"""

def usage():
    sys.stderr.write(usage_str)
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
    p1.logger = logger
    p2.logger = logger
    
    
    # create engine
    engine = Engine()
    
    # create board of default size 19
    board = Board(19)
    
    # attach everything
    engine.board = board
    engine.set_players(p1, p2)
    engine.logger = logger
    p1.engine = engine
    p2.engine = engine
    
    # create gtp_parser
    gtp = GTP(engine, logger, in_file)
        
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
