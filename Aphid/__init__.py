import re
from Aphid import objects

"""Contains all the shortcuts for searching nested items. All actions are defined in
'searches'."""


def search(iterable, searchfor, searchtype='key', **kwargs):
    """Returns first found result"""
    return objects.Search(iterable, searchfor, searchtype, **kwargs).result


def findall(iterable, searchfor, max_=0, searchtype='key', **kwargs):
    """Returns all keys/values for a key/value, default searchtype is 'key'."""
    return objects.Findall(iterable, searchfor, max_, searchtype=searchtype, **kwargs).results


def sub(iterable, searchfor, new, max_=0, searchtype='key', **kwargs):
    """Replace occurrences of 'searchfor' with 'new'. Only supports changing the dictionary value;
    not the key. 'max_' represents the max number of replacements and defaults to 0"""
    objects.Sub(iterable,searchfor, new, max_, searchtype, **kwargs)


def find_paths(iterable, searchfor, max_=0, searchtype='key', **kwargs):
    """Returns paths to 'searchfor'. If 'max_' is 0 all matches will be found"""
    return objects.FindPath(iterable, searchfor, max_, searchtype, **kwargs).paths


def find_attribute_path(cls, searchfor, max_=0, searchtype='key', **kwargs):
    """Returns paths to all matching class attributes. If 'max_' is 0 all matches will be found"""
    return objects.FindClassPaths(cls, searchfor, max_, searchtype, **kwargs).paths



