'''
implements GTP.



'''
    
import sys
import traceback
import engine
import time

# ------------------
# utility functions - TODO: put these in utils.py
# ------------------
        
class Logger(object):
    ''' cant even remember why i added all these weird functions ...'''
    def __init__(self):
        self.fname = self.genFname()
        self.f = open(self.fname, 'w')
        self.testout_only = False
    
    def __del__(self):
        self.f.flush()
        self.f.close()
    
    def log_cmd(self, s):
        self.f.write(s)
        self.f.flush()

    def set_testout_only(self):
        self.testout_only = True
        
    def log_comment(self, s):
        self.f.write("#" + s)
        self.f.flush()

    def logTestout(self, s):
        sys.stderr.write(s)
        
    def logConsole(self, s):
        if not self.testout_only:
            sys.stderr.write(s)
    
    def genFname(self):
        return "log_" + str(int(round(time.time() * 1000))) + ".txt"



class GTP(object):
    '''
    classdocs
    '''


    def __init__(self, in_file):
        '''
        Constructor
        '''
        self._logger = None
        self._engine = None
        self.testout_only = False # dont output anything to screen except test info
        self._in_file = in_file
    
    def get_line(self):
        ''' get line from stdin, using fancy pants generator approach. '''
        while True:
            line = self._in_file.readline()
            if not line:
                return
            self._logger.log_cmd(line)
            
            line = line.strip()
            pound = line.find('#')
            if pound != -1:
                line = line[:pound]
            if line:
                yield line
    
    def parse_command(self, line):
        words = line.split()
        if words[0].isdigit():
            id = words[0]
            command = words[1]
            args = words[2:]
        else:
            id = None
            command = words[0]
            args = words[1:]
        return id, command, args
    
    def send_success(self, id, response):
        ''' write 'id, response' to stdout. '''
        if self._logger.testout_only:
            return

        s = ""

        if id is not None:
            if response is not None:
                s = '=%s %s\n\n' % (id, response)
            else:
                s = '=%s\n\n' % (id,)
        else:
            if response is not None:
                s = '= %s\n\n' % (response,)
            else:
                s = '=\n\n'

        self._logger.log_comment(s)
        sys.stdout.write(s)
        sys.stdout.flush()
    
    def send_failure(self, id, error):
        ''' write 'ID, error' to stdout.'''
        if self._logger.testout_only:
            return
        s = ''
        if id is not None:
            s = '?%s %s\n\n' % (id, error)
        else:
            s = '? %s\n\n' % (error,)

        sys.stdout.write(s)
        self._logger.log_comment(s)
    
    def call_func(self, obj, name, args):
        ''' call a function called "name" on obj and return some response. '''
        member = getattr(obj, name)
        if callable(member):
            return member(*args)
        else:
            return member
    
    def get_error_str(self):
        ''' get error string from an exception. '''
        info = sys.exc_info()
        # write raw exception data to stderr for debugging - wont affect GTP/gui client
        traceback.print_exc(file=sys.stderr)
        if info[1] is None:
            return info[0]
        else:
            return str(info[1])
    
    
    def set_engine(self, engine):
        self._engine = engine
    def set_logger(self, logger):
        self._logger = logger
    def get_engine(self):
        return self._engine
    def get_logger(self):
        return self._logger
    engine = property(get_engine, set_engine)
    logger = property(get_logger, set_logger)
    ''' ------------------------------------------------------------------- ''' 
    ''' GTP commands the parser implements itself...'''
    ''' ------------------------------------------------------------------- ''' 
    def list_commands(self):
        members = dir(self._engine)
        commands = ""
        for member in members:
            if not member.startswith('_'):
                commands += member + "\n"
        return commands
    
    def protocol_version(self):
        return "666"
    
    def version(self):
        return "0.0"
    ''' ------------------------------------------------------------------- ''' 
       
    def exec_line(self, id, cmd, args):
        ''' run cmd on some object - engine,gtp-parser,etc.'''
        # do I implement this command?
        if hasattr(self, cmd):
            try:
                response = self.call_func(self, cmd, args)
                self.send_success(id, response)
            except Exception:
                error = self.get_error_str()
                self.send_failure(id, error)

        # no ... does the engine implement it?
        elif hasattr(self._engine, cmd):
            # TODO: wrap these lines in a try/catch block ...
            try:
                # try run the command and get response
                response = self.call_func(self.engine, cmd, args)
                self.send_success(id, response)
            except Exception:
                error = self.get_error_str()
                self.send_failure(id, error)
        else:
            self.send_failure(id, "unknown command")

    def run(self):
        if self._engine is None or self._in_file is None:
            raise Exception("engine or in_file not set")
        
        commands = self.list_commands()
        quit = False
        
        for line in self.get_line():
            id, command, args = self.parse_command(line)
            if command == 'quit':
                break
            else:
                self.exec_line(id, command, args)

