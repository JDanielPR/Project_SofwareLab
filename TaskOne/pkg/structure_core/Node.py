import logging
try:
    import pygame
except:
    pass
# Define some colors as global constants
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
DARK_GREEN  = (  0, 100,   0)

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
        self.towardsFirewall = [ ]
        self.towardsBarrier = [ ] 
        self.onFirewall = False
        self.onBarrier = False

    def __repr__(self):
        return "Node at {} in loadpath {}".format(self.position,
                                                  self.loadpathLevel)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.position == other.position \
               and self.loadpathLevel == other.loadpathLevel

    def __hash__(self):
        return hash(self.position) ^ hash(self.loadpathLevel)

    def draw(self, screen, offset, y_scaling):
        x = self.position + offset
        y = (self.loadpathLevel + 1) * y_scaling
        if self.onBarrier:
            pygame.draw.circle(screen, DARK_GREEN, [int(x), int(y)], int(5))
        elif self.onFirewall:
            pygame.draw.circle(screen, RED, [int(x), int(y)], int(5))
        else:
            pygame.draw.circle(screen, BLACK, [int(x), int(y)], int(5))
        

    # Method that acts on the node's position attribute to change it from one
    # place to another
    def change_position(self, deformationStep):
        '''
        Function that acts on the node's position attribute to change it from one
        place to another
        '''
##        message = "node at position {} and loadpath {} has changed its \
##position by {}"
##        logger.debug(message.format(self.position, self.loadpathLevel,
##                                    deformationStep))
        
        self.position -= deformationStep
