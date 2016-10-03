class Loadpath():
'''
Class contains it index ,all of the components within the loadpath
, and counts number of components not able to defrom
anymore.
'''
  def __init__(self):
    self.listOfComponents = [ ] 
    self.noComponentsNotDeformable= 0 

  def add_member(self, component):
    '''
    Function addes components to the list of components
    '''
    self.listOfComponents.append(component)

  def increase_noComponentsNotDeformable(self):
    '''
    Function increases number of components not able to deform
    permenantly by one
    '''
    self.noComponentsNotDeformable += 1
  def decrease_noComponentsNotDeformable(self):
    '''
    Function decreases number of components not able to defrom
    permenantly by one
    '''
    self.noComponentsNotDeformable -= 1

  

  
