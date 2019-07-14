import re
from Aphid.recursion_tools import Stack, StackTracker, Debugger


class BaseMethods:
    """Base class for methods used by interior classes"""
    def __init__(self, iterable, searchfor, searchtype='key', max_depth=0, debug=False):
        """Base settings for all instances"""
        self.iterable = iterable
        self.searchfor = searchfor
        self.searchtype = searchtype
        self.max_depth = max_depth

        ##Methods are decorated to print what they are doing if debugger is enabled
        self.debug = debug
        if debug:
            self.debug_setup()
            
        self.stack = Stack()
        if isinstance(self.searchfor, re.Pattern):  #Checking if object is a regex pattern
            self.comparision = self.regex_comparision  
        if isinstance(self.searchfor, (list, tuple)): #Checking if object is an iterable
            self.comparision = self.iter_comparision
    
    def debug_setup(self):
        """Used to setup the debugger if debug = True"""
        self.on_match = Debugger.on_match(self.on_match)
        self.recursive = Debugger.on_new_loop(self.recursive)
        if 'recursive_path' in self.__dir__():
            self.recursive_path = Debugger.on_new_loop(self.recursive_path)
        if 'recursive_class' in self.__dir__():
            self.recursive_class = Debugger.on_new_loop(self.recursive_class)
            
    def recursive(self, iterable):
        """Recursive function that loops through iterables looking for a given key/value"""
        with StackTracker(self.stack, max_depth=self.max_depth, debug=self.debug):
            if isinstance(iterable, dict):
                for key, value in iterable.items():

                    if self.comparision(key, value):
                        self.on_match(key, value, iterable)

                    if isinstance(value, (dict, list, tuple)):
                        self.recursive(value)

            if isinstance(iterable, (list, tuple)):
                for index, item in enumerate(iterable):
                    self.recursive(item)
         
    def recursive_path(self, iterable, current_path=None):
        """Recursive function that loops through iterables looking for a given key/value, and tracks the path"""
        with StackTracker(self.stack, max_depth=self.max_depth, debug=self.debug):
            if current_path is None:
                current_path = []
            
            if isinstance(iterable, dict):
                for key, value in iterable.items():
        
                    if self.comparision(key, value):
                        self.on_match(key, value, current_path + [key])
    
                    if isinstance(value, (dict, list, tuple)):
                        path = current_path + [key]
                        self.recursive_path(value, current_path=path)
    
                    elif hasattr(value, '__dict__') and not isinstance(value, (list,tuple)):
                        path = current_path + [key]
                        self.recursive_class(value, current_path=path)

            if isinstance(iterable, (list, tuple)):
                for index, item in enumerate(iterable):
                    path = current_path + [index]
                    self.recursive_path(item, path)
    
            elif hasattr(iterable, '__dict__') and not isinstance(iterable, (list,tuple)):
                path = current_path + [iterable]
                self.recursive_class(iterable, path)

    def comparision(self, key, value):
        """"Traditional comparision method"""
        if self.searchtype == 'key' and key == self.searchfor:
            return True
        elif self.searchtype == 'value' and value == self.searchfor:
            return True
        else:
            return False
        
    def regex_comparision(self, key, value):
        """"Comparision method used if 'searchfor' is a regex pattern"""
        if self.searchtype == 'key' and isinstance(key, (int, str)) and self.searchfor.search(str(key)):
            return True
        elif self.searchtype == 'value' and isinstance(value, (int, str)) and self.searchfor.search(str(value)):
            return True
        else:
            return False
    
    def iter_comparision(self, key, value):   
        """Comparision method used if 'searchfor' is an iterable"""
        
        if self.searchtype == 'key' and key in self.searchfor:
            return True
        elif self.searchtype == 'value' and value in self.searchfor:
            return True
        else:
            return False
            
    def search(self):
        """Initiates a search loop with 'recursive'. Uses StopIteration to break the recursion"""
        try:
            self.recursive(self.iterable)
        except StopIteration:
            pass

    def path_search(self):
        """Initiates a search loop with 'recursive_path'. Uses StopIteration to break the recursion"""
        try:
            self.recursive_path(self.iterable)
        except StopIteration:
            pass


class Findall(BaseMethods):
    """Find all values for a key/value, default searchtype is 'key'. Results are found from 'instance.results'"""

    def __init__(self, iterable, searchfor, max_=0, searchtype='key', **kwargs):
        BaseMethods.__init__(self, iterable, searchfor, searchtype, **kwargs)
        self.results = []
        self.found = 0
        self.max = max_
        self.search()
        
    def on_match(self, key, value, iterable):
        self.found += 1
        self.results.append((key, value))
        if self.found >= self.max != 0:
            raise StopIteration


class Search(BaseMethods):
    """Find first found result"""
    def __init__(self, iterable, searchfor, searchtype='key', **kwargs):
        BaseMethods.__init__(self, iterable, searchfor, searchtype, **kwargs)
        self.result = None
        self.search()
        
    def on_match(self, key, value, iterable):
        self.result = (key, value)
        raise StopIteration


class Sub(BaseMethods):
    """Replace occurrences of 'searchfor' with 'new'. Only supports changing the dictionary value;
    not the key. 'max' represents the max number of replacements and defaults to 0"""
    def __init__(self, iterable, searchfor, new, max_ = 0, searchtype='key', **kwargs):
        BaseMethods.__init__(self, iterable, searchfor, searchtype, **kwargs)
        self.max = max_
        self.replace = new
        self.found = 0
        self.search()
        
    def on_match(self, key, value, iterable):
        self.found += 1
        iterable[key] = self.replace
        if self.found >= self.max != 0:
            raise StopIteration


class FindPath(BaseMethods):
    """Find path to 'searchfor'. If 'max' is 0 all matches will be found"""
    def __init__(self, iterable, searchfor, max_=0, searchtype='key', **kwargs):
        BaseMethods.__init__(self, iterable, searchfor, searchtype, **kwargs)
        self.paths = []
        self.max = max_
        self.found = 0
        self.path_search()
        
    def on_match(self, key, value, path):
        self.found += 1
        self.paths.append(path)
        if self.found >= self.max and self.max != 0:
            raise StopIteration


class FindClassPaths(BaseMethods):
    """Finds a nested attribute within a class. If 'max_' is 0 all matches will be found"""
    def __init__(self, cls, searchfor, max_=0, searchtype='key', **kwargs):
        BaseMethods.__init__(self, cls, searchfor, searchtype, **kwargs)
        self.paths = []
        self.max = max_
        self.found = 0
        self.class_search()

    def on_match(self, key, value, path):
        self.found += 1
        self.paths.append(path)
        if self.found >= self.max != 0:
            raise StopIteration

    def class_search(self):
        """Kick off point for recursive class search"""
        try:
            self.recursive_class(self.iterable)
        except StopIteration:
            pass

    def recursive_class(self, cls, current_path=None):
        """Recursive function that searches a classes attributes"""
        with StackTracker(self.stack, max_depth=self.max_depth, debug=self.debug):
            if current_path == None:
                current_path = []
            
            if hasattr(cls, '__dict__') and not isinstance(cls, (list,tuple)):
                for key, value in cls.__dict__.items():
                    
    
                    if self.comparision(key, value):
                        self.on_match(key, value, current_path + [key])
    
                    if hasattr(value, '__dict__'):
                        path = current_path + [key]
                        self.recursive_class(value, path)
    
                    if isinstance(value, (dict, tuple, list)):
                        path = current_path + [key]
                        self.recursive_path(value, path)
