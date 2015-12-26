"""
Defines ReadOnly Class Property
"""


class classproperty(object):
    def __init__(self, funct_get):
        self.funct_get = funct_get

    def __get__(self, obj, owner):
        return self.funct_get(owner)