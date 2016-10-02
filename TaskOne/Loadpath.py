import member

class Loadpath():
  
  # Constructor of the class "loadpath"
  def __init__(self, n):
    self.loadpathNumber = n # Index of the loadpath
    self.listOfComponents = [ ] # List contains all the components contained \
                                # by this loadpath
    self.noOfComponents= 0 # Attributes that counts the number of components\
                            # contained by this loadpath that have reached \
                            # their deformation limit

  # Adding a new member to the loadpath
  def add_member(self, component):
    self.listOfComponents.append(component)

  # Method that modifies the attribute "noOfComponents"
  def increase_no_of_components(self): 
    self.noOfComponents += 1
  def decrease_no_of_components(self):
    self.noOfComponents -= 1

  

  
