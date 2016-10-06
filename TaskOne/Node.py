import logging

logger = logging.getLogger('node')
logging.basicConfig(level=logging.DEBUG)

class Node():
    '''
    Class that contains position of the node, its loadpath level, and the
    components it connects
    '''
    
    def __init__(self, point, loadpathLevel):
        self.position = point
        self.loadpathLevel = loadpathLevel

    # Method that acts on the node's position attribute to change it from one
    # place to another
    def change_position(self, deformationStep):
        '''
        Function that acts on the node's position attribute to change it from one
        place to another
        '''
        message = "node at position {} and loadpath {} has changed its \
position by {}"
        logger.debug(message.format(self.position, self.loadpathLevel, x))
        
        self.position += deformationStep
