Running:
--------
with a gui client (tested with GoGui on windows and linux), use the command:
python main.py --engine

to play against it on the command line:
python main.py --human

to run a file of gtp commands over the engine:
python main.py --test <some filename>


References:
-----------
GTP:
* http://www.lysator.liu.se/~gunnar/gtp/
* http://www.gnu.org/software/gnugo/gnugo_19.html

Other:
* http://en.wikipedia.org/wiki/Computer_Go


Overview of code:
-----------------
Control flow should look something like this. No idea if it currently does!

main.py:
--------
This just initialises eveything for the first time

* create engine
* create board
* create gtp_parser
* create two Player instances (AI/human/etc.)
* set: 
        engine.board_ptr = board instance
		* the ugly relationship where players knows engine, engine knows player ...
        player1.engine_ptr = engine
		player2.engine_ptr = engine
		engine.player1_ptr = player1
		engine.player2_ptr = player2
		
		gtp.engine_ptr = engine  <----- gtp now has access to every piece of information in system (hmm?)
		
* if "--human" provide on cmd line, set in_file to be stdin, otherwise, in_file = filename
       optionally change --human option to accept commands like gnugo does, rather than full GTP commands
* call gtp_run(in_file)


gtp.py:
-------
This reads a line from a file, and calls engine.run("command read from file") {basically...}
Also provides a logger, and may implement some extensions to the GTP protocol, 
eg: testing functions, that the engine doesnt really want to know about (for simplicity).


engine.py:
----------
implements the gtp functions, eg: set boardsize, 
clear_board, playmove <colour> <position>, genmove <colour>, show_board, etc. etc.

should probably provide information (read-only/const) functions such as:
* get board state
* get last move
and maybe things like ...
* is_valid_move(colour, position)


board.py:
---------
just stores the state, and nothing more. Dont check the validy of moves applied to the board. 
Eg. set_move(colour, position) will just overwrite anything there ....

players should call engine.get_board_state(), the engine then calls my_board_ptr.get_board_state() or something


player.py:
----------
interface definition for players (AI and human).
should have the functions 
* genmove() <-- generate a move if applicable  (can return null?)
* playmove() <-- updates state if the player wants to keep any state
etc. etc.

monkey.py:
----------
an AI player implementation ...
