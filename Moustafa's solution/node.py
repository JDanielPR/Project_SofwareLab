class node():
    
    def __init__(self,point):
        self.position = point
        self.loadpathLevel = 0 #this is a default value. It gonna be changed by its members
        self.connectingMembers = []

    def changePosition(self, x):
        self.position += x
        
