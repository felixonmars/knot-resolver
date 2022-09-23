"""
This type stub file was generated by pyright.
"""

import os

"""Basic infrastructure for asynchronous socket service clients and servers.

There are only two ways to have a program on a single processor do "more
than one thing at a time".  Multi-threaded programming is the simplest and
most popular way to do it, but there is another very different technique,
that lets you have nearly all the advantages of multi-threading, without
actually using multiple threads. it's really only practical if your program
is largely I/O bound. If your program is CPU bound, then preemptive
scheduled threads are probably what you really need. Network servers are
rarely CPU-bound, however.

If your operating system supports the select() system call in its I/O
library (and nearly all do), then you can use it to juggle multiple
communication channels at once; doing other work while your I/O is taking
place in the "background."  Although this strategy can seem strange and
complex, especially at first, it is in many ways easier to understand and
control than multi-threaded programming. The module documented here solves
many of the difficult problems for you, making the task of building
sophisticated high-performance network servers and clients a snap.
"""
class ExitNow(Exception):
    ...


def read(obj): # -> None:
    ...

def write(obj): # -> None:
    ...

def readwrite(obj, flags): # -> None:
    ...

def poll(timeout=..., map=...): # -> None:
    ...

def poll2(timeout=..., map=...): # -> None:
    ...

poll3 = ...
def loop(timeout=..., use_poll=..., map=..., count=...): # -> None:
    ...

class dispatcher:
    debug = ...
    connected = ...
    accepting = ...
    closing = ...
    addr = ...
    def __init__(self, sock=..., map=...) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def add_channel(self, map=...): # -> None:
        ...
    
    def del_channel(self, map=...): # -> None:
        ...
    
    def create_socket(self, family, type): # -> None:
        ...
    
    def set_socket(self, sock, map=...): # -> None:
        ...
    
    def set_reuse_addr(self): # -> None:
        ...
    
    def readable(self): # -> Literal[True]:
        ...
    
    def writable(self): # -> Literal[True]:
        ...
    
    def listen(self, num): # -> None:
        ...
    
    def bind(self, addr): # -> None:
        ...
    
    def connect(self, address): # -> None:
        ...
    
    def accept(self): # -> tuple[socket | Unknown, _RetAddress | Unknown] | None:
        ...
    
    def send(self, data): # -> int:
        ...
    
    def recv(self, buffer_size): # -> bytes:
        ...
    
    def close(self): # -> None:
        ...
    
    def __getattr__(self, attr): # -> Any:
        ...
    
    def log(self, message): # -> None:
        ...
    
    def log_info(self, message, type=...): # -> None:
        ...
    
    def handle_read_event(self): # -> None:
        ...
    
    def handle_write_event(self): # -> None:
        ...
    
    def handle_expt_event(self): # -> None:
        ...
    
    def handle_error(self): # -> None:
        ...
    
    def handle_expt(self): # -> None:
        ...
    
    def handle_read(self): # -> None:
        ...
    
    def handle_write(self): # -> None:
        ...
    
    def handle_connect(self): # -> None:
        ...
    
    def handle_accept(self): # -> None:
        ...
    
    def handle_close(self): # -> None:
        ...
    


class dispatcher_with_send(dispatcher):
    def __init__(self, sock=..., map=...) -> None:
        ...
    
    def initiate_send(self): # -> None:
        ...
    
    def handle_write(self): # -> None:
        ...
    
    def writable(self): # -> int | Literal[True]:
        ...
    
    def send(self, data): # -> None:
        ...
    


def compact_traceback(): # -> tuple[tuple[Unknown, Unknown, Unknown], Type[BaseException] | None, BaseException | None, str]:
    ...

def close_all(map=...): # -> None:
    ...

if os.name == 'posix':
    class file_wrapper:
        def __init__(self, fd) -> None:
            ...
        
        def recv(self, buffersize): # -> str:
            ...
        
        def send(self, s): # -> int:
            ...
        
        read = ...
        write = ...
        def close(self): # -> None:
            ...
        
        def fileno(self):
            ...
        
    
    
    class file_dispatcher(dispatcher):
        def __init__(self, fd, map=...) -> None:
            ...
        
        def set_file(self, fd): # -> None:
            ...