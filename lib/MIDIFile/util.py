'''
Created on 16 Sep 2019

@author: julianporter
'''
from .enum import Enum

class SafeEnum(Enum):
# class SafeEnum(enum.Enum):

    # def __init__(self):
    #     self.test = "foo"

    def __str__(self):
        return self.name.replace('_',' ')

    @classmethod
    def make(cls,n):
        try:
            return cls(n)
        except:
            return None
