import member

class Loadpath():
'''
Class contains it index ,all of the components within the loadpath
, and counts number of components not able to defrom
anymore.
'''
  def __init__(self, n):
    self.loadpathNumber = n 
    self.listOfComponents = [ ] 
    self.noOfComponents= 0 

  def add_member(self, component):
    '''
    Function addes components to the list of components
    '''
    self.listOfComponents.append(component)

  def increase_no_of_components(self):
    '''
    Function increases number of components not able to deform
    permenantly by one
    '''
    self.noOfComponents += 1
  def decrease_no_of_components(self):
    '''
    Function decreases number of components not able to defrom
    permenantly by one
    '''
    self.noOfComponents -= 1

  

  
