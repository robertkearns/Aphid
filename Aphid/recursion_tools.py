import reprlib


class StackMaxReached(Exception):
    pass


class Stack:
    """Mock stack that attempts to track the size of a call stack. For use with 'StackTracker' context manager"""
    def __init__(self):
        self.stacksize = 0

    def add(self):
        self.stacksize += 1

    def remove(self):
        self.stacksize -= 1


class StackTracker:
    """Context manager to track the size of a stack during recursions, and raise an exception
     if it exceeds 'max_size'. To use the systems default max recursion set 'max_depth' to 0
     """
    def __init__(self, stack, max_depth=0, debug=False):
        if not isinstance(stack, Stack):
            raise ValueError("StackTracker must receive a 'stack_tools.Stack' object")
        self.stack = stack
        self.max_depth = max_depth
        self.debug = debug

    def __enter__(self):
        self.stack.add()
        if self.stack.stacksize > self.max_depth != 0:
            raise StackMaxReached
        if self.debug:
            print('\n------->   Entering stack level {}\n'.format(self.stack.stacksize))

    def __exit__(self, exec_mes, exec_type, traceback):
        self.stack.remove()
        if isinstance(exec_type, StackMaxReached):
            if self.debug:
                print('__Max Stack Reached At {}__\n'.format(self.max_depth))
            return True
        if self.debug:
            print('\n<-------   Leaving stack level. Entering {}\n'.format(self.stack.stacksize))


class Debugger:
    """Container for wrapper methods. All methods here extend the functionality of the Aphid toolkit
to print what each function is doing and when. Very helpful when dealing with deep recursions, and
trying to figure out why something is not working the way it should.
"""
    
    @staticmethod
    def on_match(func):
        """Extends the 'on_match' function. This executes when there is a match. Prints the contents, and path if supplied.
Prints in format :

key           value
_______MATCH_________
[path, to, found, object]
"""
        
        def match_wrapper(*args, **kwargs):
            result = func(*args)
            print('\n  {}            {}\n__________MATCH__________\n{}'.format(args[0], args[1], args[2]))
            return result
        return match_wrapper
    
    @staticmethod
    def on_new_loop(func):
        """Prints information regarding to the new recursion. Prints the iterable underneath the stack entry phrase"""
      
        def loop_wrapper(*args, **kwargs):
            result = func(*args)
            print('Current Iterable: {}'.format(args[0]))
            if kwargs:
                print('\n{}'.format(kwargs))
            return result
        return loop_wrapper
