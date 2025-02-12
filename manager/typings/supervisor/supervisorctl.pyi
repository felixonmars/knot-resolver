"""
This type stub file was generated by pyright.
"""

import cmd
import threading

"""supervisorctl -- control applications run by supervisord from the cmd line.

Usage: %s [options] [action [arguments]]

Options:
-c/--configuration FILENAME -- configuration file path (searches if not given)
-h/--help -- print usage message and exit
-i/--interactive -- start an interactive shell after executing commands
-s/--serverurl URL -- URL on which supervisord server is listening
     (default "http://localhost:9001").
-u/--username USERNAME -- username to use for authentication with server
-p/--password PASSWORD -- password to use for authentication with server
-r/--history-file -- keep a readline history (if readline is available)

action [arguments] -- see below

Actions are commands like "tail" or "stop".  If -i is specified or no action is
specified on the command line, a "shell" interpreting actions typed
interactively is started.  Use the action "help" to find out about available
actions.
"""
class LSBInitExitStatuses:
    SUCCESS = ...
    GENERIC = ...
    INVALID_ARGS = ...
    UNIMPLEMENTED_FEATURE = ...
    INSUFFICIENT_PRIVILEGES = ...
    NOT_INSTALLED = ...
    NOT_RUNNING = ...


class LSBStatusExitStatuses:
    NOT_RUNNING = ...
    UNKNOWN = ...


DEAD_PROGRAM_FAULTS = ...
class fgthread(threading.Thread):
    """ A subclass of threading.Thread, with a kill() method.
    To be used for foreground output/error streaming.
    http://mail.python.org/pipermail/python-list/2004-May/260937.html
    """
    def __init__(self, program, ctl) -> None:
        ...
    
    def start(self): # -> None:
        ...
    
    def run(self): # -> None:
        ...
    
    def globaltrace(self, frame, why, arg): # -> (frame: Unknown, why: Unknown, arg: Unknown) -> (frame: Unknown, why: Unknown, arg: Unknown) -> Unknown | None:
        ...
    
    def localtrace(self, frame, why, arg): # -> (frame: Unknown, why: Unknown, arg: Unknown) -> Unknown:
        ...
    
    def kill(self): # -> None:
        ...
    


class Controller(cmd.Cmd):
    def __init__(self, options, completekey=..., stdin=..., stdout=...) -> None:
        ...
    
    def emptyline(self): # -> None:
        ...
    
    def default(self, line): # -> None:
        ...
    
    def exec_cmdloop(self, args, options): # -> None:
        ...
    
    def set_exitstatus_from_xmlrpc_fault(self, faultcode, ignored_faultcode=...): # -> None:
        ...
    
    def onecmd(self, line): # -> Any | None:
        """ Override the onecmd method to:
          - catch and print all exceptions
          - call 'do_foo' on plugins rather than ourself
        """
        ...
    
    def output(self, message): # -> None:
        ...
    
    def get_supervisor(self): # -> Any:
        ...
    
    def get_server_proxy(self, namespace=...): # -> Any:
        ...
    
    def upcheck(self): # -> bool:
        ...
    
    def complete(self, text, state, line=...): # -> str | None:
        """Completer function that Cmd will register with readline using
        readline.set_completer().  This function will be called by readline
        as complete(text, state) where text is a fragment to complete and
        state is an integer (0..n).  Each call returns a string with a new
        completion.  When no more are available, None is returned."""
        ...
    
    def do_help(self, arg): # -> None:
        ...
    
    def help_help(self): # -> None:
        ...
    
    def do_EOF(self, arg): # -> Literal[1]:
        ...
    
    def help_EOF(self): # -> None:
        ...
    


def get_names(inst): # -> List[Unknown]:
    ...

class ControllerPluginBase:
    name = ...
    def __init__(self, controller) -> None:
        ...
    
    doc_header = ...
    def do_help(self, arg): # -> None:
        ...
    


def not_all_langs(): # -> str | None:
    ...

def check_encoding(ctl): # -> None:
    ...

class DefaultControllerPlugin(ControllerPluginBase):
    name = ...
    listener = ...
    def do_tail(self, arg): # -> None:
        ...
    
    def help_tail(self): # -> None:
        ...
    
    def do_maintail(self, arg): # -> None:
        ...
    
    def help_maintail(self): # -> None:
        ...
    
    def do_quit(self, arg):
        ...
    
    def help_quit(self): # -> None:
        ...
    
    do_exit = ...
    def help_exit(self): # -> None:
        ...
    
    def do_status(self, arg): # -> None:
        ...
    
    def help_status(self): # -> None:
        ...
    
    def do_pid(self, arg): # -> None:
        ...
    
    def help_pid(self): # -> None:
        ...
    
    def do_start(self, arg): # -> None:
        ...
    
    def help_start(self): # -> None:
        ...
    
    def do_stop(self, arg): # -> None:
        ...
    
    def help_stop(self): # -> None:
        ...
    
    def do_signal(self, arg): # -> None:
        ...
    
    def help_signal(self): # -> None:
        ...
    
    def do_restart(self, arg): # -> None:
        ...
    
    def help_restart(self): # -> None:
        ...
    
    def do_shutdown(self, arg): # -> None:
        ...
    
    def help_shutdown(self): # -> None:
        ...
    
    def do_reload(self, arg): # -> None:
        ...
    
    def help_reload(self): # -> None:
        ...
    
    def do_avail(self, arg): # -> None:
        ...
    
    def help_avail(self): # -> None:
        ...
    
    def do_reread(self, arg): # -> None:
        ...
    
    def help_reread(self): # -> None:
        ...
    
    def do_add(self, arg): # -> None:
        ...
    
    def help_add(self): # -> None:
        ...
    
    def do_remove(self, arg): # -> None:
        ...
    
    def help_remove(self): # -> None:
        ...
    
    def do_update(self, arg): # -> None:
        ...
    
    def help_update(self): # -> None:
        ...
    
    def do_clear(self, arg): # -> None:
        ...
    
    def help_clear(self): # -> None:
        ...
    
    def do_open(self, arg): # -> None:
        ...
    
    def help_open(self): # -> None:
        ...
    
    def do_version(self, arg): # -> None:
        ...
    
    def help_version(self): # -> None:
        ...
    
    def do_fg(self, arg): # -> None:
        ...
    
    def help_fg(self, args=...): # -> None:
        ...
    


def main(args=..., options=...): # -> None:
    ...

if __name__ == "__main__":
    ...
