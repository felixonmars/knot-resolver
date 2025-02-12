"""
This type stub file was generated by pyright.
"""

API_VERSION = ...
class SupervisorNamespaceRPCInterface:
    def __init__(self, supervisord) -> None:
        ...
    
    def getAPIVersion(self): # -> Literal['3.0']:
        """ Return the version of the RPC API used by supervisord

        @return string version version id
        """
        ...
    
    getVersion = ...
    def getSupervisorVersion(self): # -> str:
        """ Return the version of the supervisor package in use by supervisord

        @return string version version id
        """
        ...
    
    def getIdentification(self):
        """ Return identifying string of supervisord

        @return string identifier identifying string
        """
        ...
    
    def getState(self): # -> dict[str, Unknown | None]:
        """ Return current state of supervisord as a struct

        @return struct A struct with keys int statecode, string statename
        """
        ...
    
    def getPID(self):
        """ Return the PID of supervisord

        @return int PID
        """
        ...
    
    def readLog(self, offset, length): # -> str:
        """ Read length bytes from the main log starting at offset

        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        """
        ...
    
    readMainLog = ...
    def clearLog(self): # -> Literal[True]:
        """ Clear the main log.

        @return boolean result always returns True unless error
        """
        ...
    
    def shutdown(self): # -> Literal[True]:
        """ Shut down the supervisor process

        @return boolean result always returns True unless error
        """
        ...
    
    def restart(self): # -> Literal[True]:
        """ Restart the supervisor process

        @return boolean result  always return True unless error
        """
        ...
    
    def reloadConfig(self): # -> list[list[list[Unknown]]]:
        """
        Reload the configuration.

        The result contains three arrays containing names of process
        groups:

        * `added` gives the process groups that have been added
        * `changed` gives the process groups whose contents have
          changed
        * `removed` gives the process groups that are no longer
          in the configuration

        @return array result  [[added, changed, removed]]

        """
        ...
    
    def addProcessGroup(self, name): # -> Literal[True]:
        """ Update the config for a running process from config file.

        @param string name         name of process group to add
        @return boolean result     true if successful
        """
        ...
    
    def removeProcessGroup(self, name): # -> Literal[True]:
        """ Remove a stopped process from the active configuration.

        @param string name         name of process group to remove
        @return boolean result     Indicates whether the removal was successful
        """
        ...
    
    def startProcess(self, name, wait=...): # -> () -> (Type[NOT_DONE_YET] | Literal[True]) | Literal[True]:
        """ Start a process

        @param string name Process name (or ``group:name``, or ``group:*``)
        @param boolean wait Wait for process to be fully started
        @return boolean result     Always true unless error

        """
        ...
    
    def startProcessGroup(self, name, wait=...): # -> (processes: Unknown = processes, predicate: Unknown = predicate, func: Unknown = func, extra_kwargs: Unknown = extra_kwargs, callbacks: Unknown = callbacks, results: Unknown = results) -> (Unknown | Type[NOT_DONE_YET]):
        """ Start all processes in the group named 'name'

        @param string name     The group name
        @param boolean wait    Wait for each process to be fully started
        @return array result   An array of process status info structs
        """
        ...
    
    def startAllProcesses(self, wait=...): # -> (processes: Unknown = processes, predicate: Unknown = predicate, func: Unknown = func, extra_kwargs: Unknown = extra_kwargs, callbacks: Unknown = callbacks, results: Unknown = results) -> (Unknown | Type[NOT_DONE_YET]):
        """ Start all processes listed in the configuration file

        @param boolean wait    Wait for each process to be fully started
        @return array result   An array of process status info structs
        """
        ...
    
    def stopProcess(self, name, wait=...): # -> () -> (Type[NOT_DONE_YET] | Literal[True]) | Literal[True]:
        """ Stop a process named by name

        @param string name  The name of the process to stop (or 'group:name')
        @param boolean wait        Wait for the process to be fully stopped
        @return boolean result     Always return True unless error
        """
        ...
    
    def stopProcessGroup(self, name, wait=...): # -> (processes: Unknown = processes, predicate: Unknown = predicate, func: Unknown = func, extra_kwargs: Unknown = extra_kwargs, callbacks: Unknown = callbacks, results: Unknown = results) -> (Unknown | Type[NOT_DONE_YET]):
        """ Stop all processes in the process group named 'name'

        @param string name     The group name
        @param boolean wait    Wait for each process to be fully stopped
        @return array result   An array of process status info structs
        """
        ...
    
    def stopAllProcesses(self, wait=...): # -> (processes: Unknown = processes, predicate: Unknown = predicate, func: Unknown = func, extra_kwargs: Unknown = extra_kwargs, callbacks: Unknown = callbacks, results: Unknown = results) -> (Unknown | Type[NOT_DONE_YET]):
        """ Stop all processes in the process list

        @param  boolean wait   Wait for each process to be fully stopped
        @return array result   An array of process status info structs
        """
        ...
    
    def signalProcess(self, name, signal): # -> Literal[True]:
        """ Send an arbitrary UNIX signal to the process named by name

        @param string name    Name of the process to signal (or 'group:name')
        @param string signal  Signal to send, as name ('HUP') or number ('1')
        @return boolean
        """
        ...
    
    def signalProcessGroup(self, name, signal): # -> Type[NOT_DONE_YET] | list[Unknown]:
        """ Send a signal to all processes in the group named 'name'

        @param string name    The group name
        @param string signal  Signal to send, as name ('HUP') or number ('1')
        @return array
        """
        ...
    
    def signalAllProcesses(self, signal): # -> Type[NOT_DONE_YET] | list[Unknown]:
        """ Send a signal to all processes in the process list

        @param string signal  Signal to send, as name ('HUP') or number ('1')
        @return array         An array of process status info structs
        """
        ...
    
    def getAllConfigInfo(self): # -> list[Unknown]:
        """ Get info about all available process configurations. Each struct
        represents a single process (i.e. groups get flattened).

        @return array result  An array of process config info structs
        """
        ...
    
    def getProcessInfo(self, name): # -> dict[str, Unknown | int | str | None]:
        """ Get info about a process named name

        @param string name The name of the process (or 'group:name')
        @return struct result     A structure containing data about the process
        """
        ...
    
    def getAllProcessInfo(self): # -> list[Unknown]:
        """ Get info about all processes

        @return array result  An array of process status results
        """
        ...
    
    def readProcessStdoutLog(self, name, offset, length): # -> str:
        """ Read length bytes from name's stdout log starting at offset

        @param string name        the name of the process (or 'group:name')
        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        """
        ...
    
    readProcessLog = ...
    def readProcessStderrLog(self, name, offset, length): # -> str:
        """ Read length bytes from name's stderr log starting at offset

        @param string name        the name of the process (or 'group:name')
        @param int offset         offset to start reading from.
        @param int length         number of bytes to read from the log.
        @return string result     Bytes of log
        """
        ...
    
    def tailProcessStdoutLog(self, name, offset, length): # -> list[str | int | bool]:
        """
        Provides a more efficient way to tail the (stdout) log than
        readProcessStdoutLog().  Use readProcessStdoutLog() to read
        chunks and tailProcessStdoutLog() to tail.

        Requests (length) bytes from the (name)'s log, starting at
        (offset).  If the total log size is greater than (offset +
        length), the overflow flag is set and the (offset) is
        automatically increased to position the buffer at the end of
        the log.  If less than (length) bytes are available, the
        maximum number of available bytes will be returned.  (offset)
        returned is always the last offset in the log +1.

        @param string name         the name of the process (or 'group:name')
        @param int offset          offset to start reading from
        @param int length          maximum number of bytes to return
        @return array result       [string bytes, int offset, bool overflow]
        """
        ...
    
    tailProcessLog = ...
    def tailProcessStderrLog(self, name, offset, length): # -> list[str | int | bool]:
        """
        Provides a more efficient way to tail the (stderr) log than
        readProcessStderrLog().  Use readProcessStderrLog() to read
        chunks and tailProcessStderrLog() to tail.

        Requests (length) bytes from the (name)'s log, starting at
        (offset).  If the total log size is greater than (offset +
        length), the overflow flag is set and the (offset) is
        automatically increased to position the buffer at the end of
        the log.  If less than (length) bytes are available, the
        maximum number of available bytes will be returned.  (offset)
        returned is always the last offset in the log +1.

        @param string name         the name of the process (or 'group:name')
        @param int offset          offset to start reading from
        @param int length          maximum number of bytes to return
        @return array result       [string bytes, int offset, bool overflow]
        """
        ...
    
    def clearProcessLogs(self, name): # -> Literal[True]:
        """ Clear the stdout and stderr logs for the named process and
        reopen them.

        @param string name   The name of the process (or 'group:name')
        @return boolean result      Always True unless error
        """
        ...
    
    clearProcessLog = ...
    def clearAllProcessLogs(self): # -> () -> (Type[NOT_DONE_YET] | list[Unknown]):
        """ Clear all process log files

        @return array result   An array of process status info structs
        """
        ...
    
    def sendProcessStdin(self, name, chars): # -> Literal[True]:
        """ Send a string of chars to the stdin of the process name.
        If non-7-bit data is sent (unicode), it is encoded to utf-8
        before being sent to the process' stdin.  If chars is not a
        string or is not unicode, raise INCORRECT_PARAMETERS.  If the
        process is not running, raise NOT_RUNNING.  If the process'
        stdin cannot accept input (e.g. it was closed by the child
        process), raise NO_FILE.

        @param string name        The process name to send to (or 'group:name')
        @param string chars       The character data to send to the process
        @return boolean result    Always return True unless error
        """
        ...
    
    def sendRemoteCommEvent(self, type, data): # -> Literal[True]:
        """ Send an event that will be received by event listener
        subprocesses subscribing to the RemoteCommunicationEvent.

        @param  string  type  String for the "type" key in the event header
        @param  string  data  Data for the event body
        @return boolean       Always return True unless error
        """
        ...
    


def make_allfunc(processes, predicate, func, **extra_kwargs): # -> (processes: Unknown = processes, predicate: Unknown = predicate, func: Unknown = func, extra_kwargs: Unknown = extra_kwargs, callbacks: Unknown = callbacks, results: Unknown = results) -> (Unknown | Type[NOT_DONE_YET]):
    """ Return a closure representing a function that calls a
    function for every process, and returns a result """
    ...

def isRunning(process): # -> bool:
    ...

def isNotRunning(process): # -> bool:
    ...

def isSignallable(process): # -> Literal[True] | None:
    ...

def make_main_rpcinterface(supervisord): # -> SupervisorNamespaceRPCInterface:
    ...
