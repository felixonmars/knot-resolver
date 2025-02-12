"""
This type stub file was generated by pyright.
"""

def process_or_group_name(name): # -> str:
    """Ensures that a process or group name is not created with
       characters that break the eventlistener protocol or web UI URLs"""
    ...

def integer(value): # -> int:
    ...

TRUTHY_STRINGS = ...
FALSY_STRINGS = ...
def boolean(s): # -> bool:
    """Convert a string value to a boolean value."""
    ...

def list_of_strings(arg): # -> list[Unknown]:
    ...

def list_of_ints(arg): # -> list[int]:
    ...

def list_of_exitcodes(arg): # -> list[int]:
    ...

def dict_of_key_value_pairs(arg): # -> dict[Unknown, Unknown]:
    """ parse KEY=val,KEY2=val2 into {'KEY':'val', 'KEY2':'val2'}
        Quotes can be used to allow commas in the value
    """
    ...

class Automatic:
    ...


class Syslog:
    """TODO deprecated; remove this special 'syslog' filename in the future"""
    ...


LOGFILE_NONES = ...
LOGFILE_AUTOS = ...
LOGFILE_SYSLOGS = ...
def logfile_name(val): # -> Type[Automatic] | Type[Syslog] | None:
    ...

class RangeCheckedConversion:
    """Conversion helper that range checks another conversion."""
    def __init__(self, conversion, min=..., max=...) -> None:
        ...
    
    def __call__(self, value):
        ...
    


port_number = ...
def inet_address(s): # -> tuple[Unknown | Literal[''], Unknown]:
    ...

class SocketAddress:
    def __init__(self, s) -> None:
        ...
    


class SocketConfig:
    """ Abstract base class which provides a uniform abstraction
    for TCP vs Unix sockets """
    url = ...
    addr = ...
    backlog = ...
    def __repr__(self): # -> str:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __ne__(self, other) -> bool:
        ...
    
    def get_backlog(self): # -> None:
        ...
    
    def addr(self):
        ...
    
    def create_and_bind(self):
        ...
    


class InetStreamSocketConfig(SocketConfig):
    """ TCP socket config helper """
    host = ...
    port = ...
    def __init__(self, host, port, **kwargs) -> None:
        ...
    
    def addr(self): # -> tuple[Unknown | None, Unknown | None]:
        ...
    
    def create_and_bind(self): # -> socket:
        ...
    


class UnixStreamSocketConfig(SocketConfig):
    """ Unix domain socket config helper """
    path = ...
    mode = ...
    owner = ...
    sock = ...
    def __init__(self, path, **kwargs) -> None:
        ...
    
    def addr(self): # -> Unknown | None:
        ...
    
    def create_and_bind(self): # -> socket:
        ...
    
    def get_mode(self): # -> None:
        ...
    
    def get_owner(self): # -> None:
        ...
    


def colon_separated_user_group(arg): # -> tuple[int, int]:
    """ Find a user ID and group ID from a string like 'user:group'.  Returns
        a tuple (uid, gid).  If the string only contains a user like 'user'
        then (uid, -1) will be returned.  Raises ValueError if either
        the user or group can't be resolved to valid IDs on the system. """
    ...

def name_to_uid(name): # -> int:
    """ Find a user ID from a string containing a user name or ID.
        Raises ValueError if the string can't be resolved to a valid
        user ID on the system. """
    ...

def name_to_gid(name): # -> int:
    """ Find a group ID from a string containing a group name or ID.
        Raises ValueError if the string can't be resolved to a valid
        group ID on the system. """
    ...

def gid_for_uid(uid): # -> int:
    ...

def octal_type(arg): # -> int:
    ...

def existing_directory(v):
    ...

def existing_dirpath(v):
    ...

def logging_level(value): # -> Any:
    ...

class SuffixMultiplier:
    def __init__(self, d, default=...) -> None:
        ...
    
    def __call__(self, v): # -> int:
        ...
    


byte_size = ...
def url(value):
    ...

SIGNUMS = ...
def signal_number(value): # -> int | Any:
    ...

class RestartWhenExitUnexpected:
    ...


class RestartUnconditionally:
    ...


def auto_restart(value): # -> Type[RestartUnconditionally] | Type[RestartWhenExitUnexpected] | str | Literal[False]:
    ...

def profile_options(value): # -> tuple[list[Unknown], bool]:
    ...
