import imp
import initialization
import setAnimation
from abc import ABCMeta, abstractmethod

imp.reload(initialization)   #Load library
imp.reload(setAnimation)

class LoadPath:
    __metaclass__ = ABCMeta

    @abstractmethod
    def addMember(self): pass

class horizontalLoadPath(LoadPath):
    def __init__(self , level):
        self.level = level
        self.path = []

    def addMember(self, obj):
        self.path.append(obj)
        
    def getNumberOfMembers(self):
        return len(self.path) 