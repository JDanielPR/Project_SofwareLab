class member():
  
  def __init__(self,x,y,z,nome,lm):
    self.leftnode = x
    self.rightnode = y
    self.dlength = self.calLength()*z
    self.length = self.calLength()
    self.name = nome
    self.leftmember = lm
    self.state = True
    
  def calLength(self):
    return abs(self.leftnode - self.rightnode)

  def deform(self,x):
    self.leftnode += x
    if self.leftmember != None:
      self.transmotion(x)

  def transmotion(self,x):
    self.leftmember.movemember(x)

  def movemember(x):
    self.leftmember.leftnode += x
    self.leftmember.rightnode += x
    self.leftmember.transmotion(x)

  def changestate(self,switch):
    self.state = switch
