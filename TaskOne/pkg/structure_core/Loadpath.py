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

  def valid_components(self):
    # if there are valid gaps
    valid_gaps = [comp for comp in self.listComponents
                  if comp.isGap
                  and comp.connectedToBarrier
                  and comp.connectedToFirewall
                  and comp.deformable_length() > 0]
    if any(valid_gaps):
      # return a list with only the one closer to the barrier
      valid_gaps.sort(key=lambda gap: gap.leftNode.position)
      return [valid_gaps[0]]
    
    # else
    # return all the valid components (gaps included)
    return [comp
            for comp in self.listComponents
            if comp.connectedToBarrier
            and comp.connectedToFirewall]
  
  
