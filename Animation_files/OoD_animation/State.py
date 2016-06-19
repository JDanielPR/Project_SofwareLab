import imp
import math
import bpy   #Module for blender
from abc import ABCMeta, abstractmethod
import Member
import LoadPath
import MemberMassimo

imp.reload(Member)
imp.reload(LoadPath)
imp.reload(MemberMassimo)
'''
class State:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getStatus(self): pass

class InitialState(State):
    def __init__(self, structure):
        
'''        
       
        