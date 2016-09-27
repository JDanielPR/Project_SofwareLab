import member

class loadpath():
  
  #Constructor of the class "loadpath"
  def __init__(self, n):
    self.loadpathNumber = n
    self.listOfMembers = []
    self.noOffMembers = 0

  #Adding a new member to the loadpath
  def addMember(self, mem):
    self.listOfMembers.append(mem)

  #STATIC method that modifies the static member "noOffMembers"
  def increaseNoOffMembers(self):
    self.noOffMembers += 1
  def decreaseNoOffMembers(self):
    self.noOffMembers -=1

  

  
