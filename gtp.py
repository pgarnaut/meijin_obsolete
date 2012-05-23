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


    def __init__(self, engine, logger, in_file=sys.stdin):
        '''
        Constructor
        '''
        self._logger = logger
        self._engine = engine
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
    
    def parse_line(self, line):
        words = line.split()
        if words[0].isdigit():
            id_ = words[0]
            command = words[1]
            args = words[2:]
        else:
            id_ = None
            command = words[0]
            args = words[1:]
        return id_, command, args
    
    def build_failure_str(self, id_, error):
        if self._logger.testout_only:
            return
        s = ''
        if id_ is not None:
            s = '?%s %s\n\n' % (id_, error)
        else:
            s = '? %s\n\n' % (error,)

        #sys.stdout.write(s)
        #self._logger.log_comment(s)
        return s
    
    def build_happy_str(self, id_, response):
        ''' write 'id, response' to stdout. '''
        s = ""

        if id_ is not None:
            if response is not None:
                s = '=%s %s\n\n' % (id_, response)
            else:
                s = '=%s\n\n' % (id_,)
        else:
            if response is not None:
                s = '= %s\n\n' % (response,)
            else:
                s = '=\n\n'

        return s
        
    def call_func(self, obj, id_, name, args):
        ''' call a function called "name" on obj and return some response. '''
        member = getattr(obj, name)
        response = member #default
        if callable(member):
            try:
                response = self.build_happy_str(id_, member(*args))
            except Exception:
                response = self.build_failure_str(id_, self.get_error_str())
        
        return response
        
    
    def get_error_str(self):
        ''' get error string from an exception. '''
        info = sys.exc_info()
        # write raw exception data to stderr for debugging - wont affect GTP/gui client
        traceback.print_exc(file=sys.stderr)
        if info[1] is None:
            return info[0]
        else:
            return str(info[1])
    
    def write_response(self, s):
        sys.stdout.write(s)
        sys.stdout.flush()
        self._logger.log_comment(s)
        
    @property
    def engine(self):
        return self._engine
    @property
    def logger(self):
        return self._logger

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
        
    def exec_line(self, id_, cmd, args):
        ''' run cmd on some object - engine,gtp-parser,etc.'''
        
        # do I implement this command?
        if hasattr(self, cmd):
            response = self.call_func(self, id_, cmd, args)
            #self._logger.log_comment(response)
            self.write_response(response)

        # no ... does the engine implement it?
        elif hasattr(self._engine, cmd):
            response = self.call_func(self.engine, id_, cmd, args)
            self.write_response(response)
            
        else:
            self.write_response(self.build_failure_str(id_, "unknown command"))
            

    def run(self):        
        for line in self.get_line():
            id_, command, args = self.parse_line(line)
            if command == 'quit':
                break
            else:
                self.exec_line(id_, command, args)

