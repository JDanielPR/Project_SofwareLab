import logging

logger = logging.getLogger('node')

class node():
    
    def __init__(self,point):
        self.position = point
        self.loadpathLevel = 0 #this is a default value. It gonna be changed by its members
        self.connectingMembers = []

    def changePosition(self, x):
        logger.debug("node at position {} and loadpath {} has changed its position by {}".format(self.position,self.loadpathLevel,x))
        self.position += x
        
