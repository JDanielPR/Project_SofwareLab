class BlenderTags():
    def __init__(self , nodeNumber = 0 , xCoordinate = 0.0 , yCoordinate = 0.0):
        self.nodeNumber = nodeNumber 
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
    def get_nodeNumber (self):
        return self.nodeNumber 
    def get_xCoordinate(self):
        return self.xCoordinate
    def get_yCoordinate(self):
        return self.yCoordinate