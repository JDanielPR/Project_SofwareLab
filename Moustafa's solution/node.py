class node():
    
    def __init__(self,point):
        self.position = point
        self.connectingMembers = []

    def changePosition(self, x):
        self.position += x
        
