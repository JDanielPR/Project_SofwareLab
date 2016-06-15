class member():

  def __init__(self,x,y,z,nome,lm):
    self.leftNode = x
    self.rightNode = y
    self.dLength = (self.calLength())*z
    self.length = self.calLength()
    self.name = nome
    self.leftMember = lm
    self.state = True
    self.rigidLength = (self.length)*(1-z)
    self.deformPossibility = True
    
  def calLength(self):
    return abs(self.leftNode.position - self.rightNode.position)

  def deform(self,x):
    self.leftNode.changePosition (x)
    self.changeDeformLength(x)
    if self.leftMember != None:
      self.leftMember.transmotion(x)

  def changeDeformLength(self, change):
    self.dLength -= change

  def transmotion(self,x):
    if self.leftMember != None: 
      self.leftMember.leftNode.changePosition(x)
      self.leftMember.transmotion(x)

  def changeState(self,switch):
    self.state = switch

  def canDeform(self, state):
    self.deformPossibility = state
