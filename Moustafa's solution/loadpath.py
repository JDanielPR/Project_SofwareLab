import member

class loadpath():

  def __init__(self, n):
    self.LoadpathNumber = n
    self.ListOfMembers = []

  def addMember(self, mem):
    self.ListOfMembers.append(mem)
