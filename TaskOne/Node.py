import logging

logger = logging.getLogger('node')
logging.basicConfig(level=logging.DEBUG)

class Node():
    
    def __init__(self,point):
       #Location of the node at the respective loadpath
        self.position = point
        #Level of loadpath the node belongs to. It has a default value, and it will be changed by its members
        self.loadpathLevel = 0
        #List contains all members that are connected through the node object
        self.connectingMembers = []

    #Method that acts on the node's position attribute to change it from one place to another
    def changePosition(self, deformationStep):
        logger.debug("node at position {} and loadpath {} has changed its position by {}".format(self.position,self.loadpathLevel,x))
        self.position += deformationStep
