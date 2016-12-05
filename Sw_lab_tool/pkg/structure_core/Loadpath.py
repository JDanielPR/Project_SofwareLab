from . import component

class Loadpath():
  """Groups all components and nodes at the same loadpath level."""
  
  def __init__(self, level):
    """Constructor of the class structure_core.loadpath.Loadpath.

    Args:
      level:
        an integer, that identifies the loadpath level
    Returns:
      an object of the class.
    Raises:
      nothing is raised.
    """
    self.listComponents = [ ]
    self.setNodes = set()
    self.level = level

##  def add_member(self, component):
##    """Function addes components to the list of components
##    """
##    self.listComponents.append(component)

  def valid_components(self):
    """Returns a list with the current components allowed to deform.

    Args:
      nothing is taken
    Returns:
      nothing is returned
    Raises:
      nothing is raised.
    """
    # collect in a list all the components allowed to deform
    validComps = [comp
                  for comp in self.listComponents
                  if comp.deformable_length() > 0]
    # gaps priority
    if any(validComps) \
       and all(comp.isGap for comp in validComps):
      # if there is any valid component and they are all gaps
      # return a list with the most left one
      return [min(validComps,
                  key = lambda gap: gap.leftNode.position)]
    else:
      # otherwise return all of them
      return validComps

##  def add_node(self, node):
##    """Creates gaps to add the node to the loadpath.
##
##If the loadpath is empty a second node must be given."""
##    
##    loadpath_nodes = set(comp.leftNode for comp in self.listComponents) \
##                         | set(comp.rightNode for comp in self.listComponents)
##    
##    # CASE 1: empty loadpath
##    if not loadpath_nodes:
##      # the loadpath is empty
##      # create and append gap
##      gap = Component.Component(node, node, 0, "gap", True) # the gap is
##                                                            # already closed
##      self.listComponents.append(gap)
##        
##    # CASE 2: proper loadpath
##    else:
##      # if the node is in the same position of a loadpath node, keep on,
##      # considering the latter
##      if node.position in [node.position for node in loadpath_nodes]:
##        node, = [n for n in loadpath_nodes
##                 if node.position == n.position]
##      # ensure that the node doesn't divide any component (gaps excluded)
##      assert not any(comp.leftNode.position <
##                     node.position <
##                     comp.rightNode.position
##                     for comp in self.listComponents
##                     if not comp.isGap)
##      # look for a gap cut by the given node
##      try:
##        cut_gap, = [gap
##                    for gap in self.listComponents
##                    if gap.isGap
##                    and
##                    gap.leftNode.position <
##                    node.position <
##                    rightNode.position]
##      except ValueError:
##        cut_gap = False
##
##      # if any
##      if cut_gap:
##        # forget it
##        self.listComponents.remove(cut_gap)
##        cut_gap.leftNode.towardsFirewall.remove(cut_gap)
##        cut_gap.rightNode.towardsBarrier.remove(cut_gap)
##        # get previous and next node
##        previous_node = cut_gap.leftNode
##        next_node = cut_gap.rightNode
##      # else
##      else:
##        # look for previous and next node
##        previous_node = max((n for n in loadpath_nodes
##                             if n.position < node.position),
##                            key = lambda n: n.position)
##        next_node = min((n for n in loadpath_nodes
##                         if node.position < n.position),
##                        key = lambda n: n.position)
##        # at least one should be found
##        assert previous_node or next_node
##        
##      # create and append gaps
##      if previous_node:
##        if any(comp.leftNode is previous_node
##               for comp in node.towardsBarrier):
##          # there is already a component going from previous_node to node
##          pass
##        else:
##          gap = Component.Component(previous_node, node, 0, "gap", True)
##          self.listComponents.append(gap)
##      if next_node:
##        if any(comp.rightNode is next_node
##               for comp in node.towardsFirewall):
##          # there is already a component going from previous_node to node
##          pass
##        else:
##          gap = Component.Component(node, next_node, 0, "gap", True)
##          self.listComponents.append(gap)
