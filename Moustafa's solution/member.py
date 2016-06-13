class member():
  
  def __init__(self,x,y,z,nome,lm):
    self.leftnode = x
    self.rightnode = y
    self.dlength = self.calLength()*z
    self.length = self.calLength()
    self.name = nome
    self.leftmember = lm
    self.state = True
    self.rigidlength = (self.length)*(1-z)
    self.deformPossibility = True
    
  def calLength(self):
    return abs(self.leftnode - self.rightnode)

  def deform(self,x):
    self.leftnode += x
    self.changedlength(x)
    if self.leftmember != None:
      self.leftmember.transmotion(x)

  def changedlength(self, d):
    change = d
    self.dlength -= change

  def transmotion(self,x):
    if self.leftmember != None: 
      self.leftmember.leftnode += x
      self.leftmember.rightnode += x
      self.leftmember.transmotion(x)

  def changestate(self,switch):
    self.state = switch

  def canDeform(self, state):
    self.deformPossibility = state
