import os
import logging
import inspect


def init_logger( app ):
    pass

def log( msg ):
    stack = inspect.stack()[1]
    fyle = os.path.basename( stack[1] ) 
    msg =  'Error: {} @ {}:{}'.format (msg, fyle, stack[2] )
    print msg
    return msg 

