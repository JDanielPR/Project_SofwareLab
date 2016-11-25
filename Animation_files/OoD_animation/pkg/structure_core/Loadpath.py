from . import Component

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
            if (comp.connectedToBarrier
            and comp.connectedToFirewall)
            or comp.isGap]

  def add_node(self, node):
    """Creates gaps to add the node to the loadpath.

If the loadpath is empty a second node must be given."""
    
    loadpath_nodes = set(comp.leftNode for comp in self.listComponents) \
                         | set(comp.rightNode for comp in self.listComponents)
    
    # CASE 1: empty loadpath
    if not loadpath_nodes:
      # the loadpath is empty
      # create and append gap
      gap = Component.Component(node, node, 0, "gap", True) # the gap is
                                                            # already closed
      self.listComponents.append(gap)
        
    # CASE 2: proper loadpath
    else:
      # if the node is in the same position of a loadpath node, keep on,
      # considering the latter
      if node.position in [node.position for node in loadpath_nodes]:
        node, = [n for n in loadpath_nodes
                 if node.position == n.position]
      # ensure that the node doesn't divide any component (gaps excluded)
      assert not any(comp.leftNode.position <
                     node.position <
                     comp.rightNode.position
                     for comp in self.listComponents
                     if not comp.isGap)
      # look for a gap cut by the given node
      try:
        cut_gap, = [gap
                    for gap in self.listComponents
                    if gap.isGap
                    and
                    gap.leftNode.position <
                    node.position <
                    rightNode.position]
      except ValueError:
        cut_gap = False

      # if any
      if cut_gap:
        # forget it
        self.listComponents.remove(cut_gap)
        cut_gap.leftNode.towardsFirewall.remove(cut_gap)
        cut_gap.rightNode.towardsBarrier.remove(cut_gap)
        # get previous and next node
        previous_node = cut_gap.leftNode
        next_node = cut_gap.rightNode
      # else
      else:
        # look for previous and next node
        previous_node = max((n for n in loadpath_nodes
                             if n.position < node.position),
                            key = lambda n: n.position)
        next_node = min((n for n in loadpath_nodes
                         if node.position < n.position),
                        key = lambda n: n.position)
        # at least one should be found
        assert previous_node or next_node
        
      # create and append gaps
      if previous_node:
        if any(comp.leftNode is previous_node
               for comp in node.towardsBarrier):
          # there is already a component going from previous_node to node
          pass
        else:
          gap = Component.Component(previous_node, node, 0, "gap", True)
          self.listComponents.append(gap)
      if next_node:
        if any(comp.rightNode is next_node
               for comp in node.towardsFirewall):
          # there is already a component going from previous_node to node
          pass
        else:
          gap = Component.Component(node, next_node, 0, "gap", True)
          self.listComponents.append(gap)
