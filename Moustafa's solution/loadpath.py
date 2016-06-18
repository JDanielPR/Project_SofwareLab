import member

class loadpath():

  def __init__(self, n):
    self.loadpathNumber = n
    self.listOfMembers = []

  def addMember(self, mem):
    self.listOfMembers.append(mem)
