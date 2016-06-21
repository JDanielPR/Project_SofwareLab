class crossMember():

  def __init__(self, nodeOne, nodeTwo, defLength):

    self.firstNode = nodeOne  #the first node is chosen as the one closest to the barrier 
    self.secondNode = nodeTwo
    self.horizDefLength = defLength
    self.originalHorizDiffOfNodes = self.firstNode.position - self.secondNode.position#this number is always Negative

    self.NoContNoElong = False  #if this is True, then the member should not have any relative motion between its two nodes
    

  def changeNoContNoElong(self, newValue):
    self.NoContNoElong = newValue


#this function checks the configuration of the crossMember after the carried out branch of elementTree
#if this cofiguration violates our assumptions, then it will return False, otherwise True
  def checkNewCrossMembConfig(self):

    returnValue = True

    CurrentHorizDiffOfNodes = self.firstNode.position - self.secondNode.position
    
    if self.NoContNoElong == False
      diffCurrentAndOriginal = abs(self.originalHorizDiffOfNodes)  -abs(CurrentHorizDiffOfNodes)
      if diffCurrentAndOriginal > self.horizDefLength or CurrentHorizDiffOfNodes >= 0:
        returnValue = False

      if diffCurrentAndOriginal == self.horizDefLength:
        self.NoContNoElong = True

      return returnValue

    else:
      if abs(CurrentHorizDiffOfNodes) != self.horizDefLength:
        returnValue = False
        return returnValue

