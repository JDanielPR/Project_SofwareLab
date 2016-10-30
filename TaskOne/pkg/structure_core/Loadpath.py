class Loadpath():
  '''Class contains it index ,all of the components within the loadpath, and
counts number of components not able to defrom anymore.'''
  def __init__(self):
    self.listComponents = [ ]

  def add_member(self, component):
    '''
    Function addes components to the list of components
    '''
    self.listComponents.append(component)


  
