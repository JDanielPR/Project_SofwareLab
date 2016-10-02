import member

class Loadpath():
  
  #Constructor of the class "loadpath"
  def __init__(self, n):
    self.loadpathNumber = n #Index of the loadpath
    self.listOfComponents = []    #List contains all the components contained by this loadpath
    self.noOffComponents= 0     #Attributes that counts the number of components contained by this loadpath that have reached their deformation limit

  #Adding a new member to the loadpath
  def addMember(self, component):
    self.listOfComponents.append(component)

  #Method that modifies the attribure "noOffMembers"
  def increaseNoOffComponents(self): 
    self.noOffComponents += 1
  def decreaseNoOffComponents(self):
    self.noOffComponents -=1

  

  
