"""
This type stub file was generated by pyright.
"""

from supervisor.medusa import http_server
from supervisor.medusa.auth_handler import auth_handler

class NOT_DONE_YET:
    ...


class deferring_chunked_producer:
    """A producer that implements the 'chunked' transfer coding for HTTP/1.1.
    Here is a sample usage:
            request['Transfer-Encoding'] = 'chunked'
            request.push (
                    producers.chunked_producer (your_producer)
                    )
            request.done()
    """
    def __init__(self, producer, footers=...) -> None:
        ...
    
    def more(self): # -> Type[NOT_DONE_YET] | bytes:
        ...
    


class deferring_composite_producer:
    """combine a fifo of producers into one"""
    def __init__(self, producers) -> None:
        ...
    
    def more(self): # -> Type[NOT_DONE_YET] | Literal[b'']:
        ...
    


class deferring_globbing_producer:
    """
    'glob' the output from a producer into a particular buffer size.
    helps reduce the number of calls to send().  [this appears to
    gain about 30% performance on requests to a single channel]
    """
    def __init__(self, producer, buffer_size=...) -> None:
        ...
    
    def more(self): # -> Type[NOT_DONE_YET] | bytes:
        ...
    


class deferring_hooked_producer:
    """
    A producer that will call <function> when it empties,.
    with an argument of the number of bytes produced.  Useful
    for logging/instrumentation purposes.
    """
    def __init__(self, producer, function) -> None:
        ...
    
    def more(self): # -> Type[NOT_DONE_YET] | Literal[b'']:
        ...
    


class deferring_http_request(http_server.http_request):
    """ The medusa http_request class uses the default set of producers in
    medusa.producers.  We can't use these because they don't know anything
    about deferred responses, so we override various methods here.  This was
    added to support tail -f like behavior on the logtail handler """
    def done(self, *arg, **kw): # -> None:
        """ I didn't want to override this, but there's no way around
        it in order to support deferreds - CM

        finalize this transaction - send output to the http channel"""
        ...
    
    def log(self, bytes): # -> None:
        """ We need to override this because UNIX domain sockets return
        an empty string for the addr rather than a (host, port) combination """
        ...
    
    def cgi_environment(self): # -> dict[Unknown, Unknown]:
        ...
    
    def get_server_url(self): # -> str:
        """ Functionality that medusa's http request doesn't have; set an
        attribute named 'server_url' on the request based on the Host: header
        """
        ...
    


class deferring_http_channel(http_server.http_channel):
    ac_out_buffer_size = ...
    delay = ...
    last_writable_check = ...
    def writable(self, now=...): # -> bool:
        ...
    
    def refill_buffer(self): # -> None:
        """ Implement deferreds """
        ...
    
    def found_terminator(self): # -> None:
        """ We only override this to use 'deferring_http_request' class
        instead of the normal http_request class; it sucks to need to override
        this """
        ...
    


class supervisor_http_server(http_server.http_server):
    channel_class = deferring_http_channel
    ip = ...
    def prebind(self, sock, logger_object): # -> None:
        """ Override __init__ to do logger setup earlier so it can
        go to our logger object instead of stdout """
        ...
    
    def postbind(self): # -> None:
        ...
    
    def log_info(self, message, type=...): # -> None:
        ...
    


class supervisor_af_inet_http_server(supervisor_http_server):
    """ AF_INET version of supervisor HTTP server """
    def __init__(self, ip, port, logger_object) -> None:
        ...
    


class supervisor_af_unix_http_server(supervisor_http_server):
    """ AF_UNIX version of supervisor HTTP server """
    def __init__(self, socketname, sockchmod, sockchown, logger_object) -> None:
        ...
    
    def checkused(self, socketname): # -> bool:
        ...
    


class tail_f_producer:
    def __init__(self, request, filename, head) -> None:
        ...
    
    def __del__(self): # -> None:
        ...
    
    def more(self): # -> bytes | Type[NOT_DONE_YET] | Literal['''==> File truncated <==
''']:
        ...
    


class logtail_handler:
    IDENT = ...
    path = ...
    def __init__(self, supervisord) -> None:
        ...
    
    def match(self, request):
        ...
    
    def handle_request(self, request): # -> None:
        ...
    


class mainlogtail_handler:
    IDENT = ...
    path = ...
    def __init__(self, supervisord) -> None:
        ...
    
    def match(self, request):
        ...
    
    def handle_request(self, request): # -> None:
        ...
    


def make_http_servers(options, supervisord): # -> list[Unknown]:
    ...

class LogWrapper:
    '''Receives log messages from the Medusa servers and forwards
    them to the Supervisor logger'''
    def __init__(self, logger) -> None:
        ...
    
    def log(self, msg): # -> None:
        '''Medusa servers call this method.  There is no log level so
        we have to sniff the message.  We want "Server Error" messages
        from medusa.http_server logged as errors at least.'''
        ...
    


class encrypted_dictionary_authorizer:
    def __init__(self, dict) -> None:
        ...
    
    def authorize(self, auth_info): # -> Literal[False]:
        ...
    


class supervisor_auth_handler(auth_handler):
    def __init__(self, dict, handler, realm=...) -> None:
        ...
