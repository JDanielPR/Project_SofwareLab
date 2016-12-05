import xml.etree.ElementTree as et
from .structure_core import structure
from .structure_core import loadpath
from .structure_core import component
from .structure_core import cross_component
from .structure_core import node
from itertools import tee



def read_xml(path):
    """Return a Structure object, based on the .xml at the given path.

    Args:
      path:
        a string, that contains the path to the .xml file
    Returns:
      an object of the class structure_core.structure.Structure.
    Raises:
      nothing is raised.
    """
    # create a tree object, given the address of the .xml file
    tree = et.parse(path)
    # create a variable that contains the root
    root = tree.getroot()
    # create empty structure
    struct = structure.Structure([ ],[ ])
    # add nodes to loadpaths
    add_nodes(root, struct)
    # add components to loadpaths and cross components to the structure
    add_components(root, struct)
    # insert gaps
    gaps_insertor(struct)
    # initialise firewall and barrier
    init_firewall_and_barrier(struct)
    return struct

def add_nodes(root, struct):
    """Add nodes to the structure, given the root of the tree to parse.

    Every node is added to the correct loadpath defined in
    struct.listLoadpaths.
    
    Args:
      root:
        the root of the tree to parse given by the ElementTree.getroot()
        function.
      struct:
        the structure_core.structure.Structure obj
    Returns:
      nothing is returned.
    Raises:
      nothing is raised.
    """
    # loop over levels (i.e. loadpath levels)
    for level in root.iter('level'):
        # create a loadpath
        level_id = int(level.find('id').text)
        lp = loadpath.Loadpath(level_id)
        # loop over components to add nodes
        for component in level.iter('component'):
            if component.find('end_level') is None: # skip crossComponents
                x = float(component.find('x1').text)
                lp.setNodes.add(node.Node(x, level_id))
                x = float(component.find('x2').text)        
                lp.setNodes.add(node.Node(x, level_id))
        # append loadpath
        if lp.setNodes:
            struct.listLoadpaths.append(lp)
    # loop over cross components
    for component in root.iter('component'):
        if component.find('end_level') is not None:
            # look for loadpaths defined implicitly by "end_level" 
            level_id = int(component.find('end_level').text)
            try:
                lp, = [loadpath for loadpath in struct.listLoadpaths
                             if loadpath.level == level_id]
            except ValueError:
                # no such a loadpath, create it
                lp = loadpath.Loadpath(level_id)
                # append loadpath
                struct.listLoadpaths.append(lp)
            # add node
            x = float(component.find('x2').text)
            lp.setNodes.add(node.Node(x, level_id))

def add_components(root, struct):
    """Add components to the structure, given the root of the tree to parse.

    Every compoenent is added to the correct loadpath defined in
    struct.listLoadpaths. The loadpath must already contain the left and the
    right node of each component.

    Args:
      root:
        the root of the tree to parse given by the ElementTree.getroot()
        function.
      struct:
        the structure_core.structure.Structure obj
    Returns:
      nothing is returned.
    Raises:
      nothing is raised.
    """
    # loop over components
    for level in root.iter('level'):
        level_id = int(level.find('id').text)
        for comp in level.iter('component'):
            # if it's a normal component
            if comp.find('end_level') is None:
                # get loadpath
                loadpath, = [loadpath for loadpath in struct.listLoadpaths
                             if loadpath.level == level_id]
                # get nodes
                leftNode, = [node for node in loadpath.setNodes
                             if node.position == float(comp.
                                                       find('x1').text)]
                rightNode, = [node for node in loadpath.setNodes
                              if node.position == float(comp.
                                                        find('x2').text)]
                if rightNode.position < leftNode.position:
                    leftNode, rightNode = rightNode, leftNode
                # compute rigid length
                length = rightNode.position - leftNode.position
                rigidLength = length - float(comp.find('defoLength').text)
                # create and append component
                loadpath.listComponents.append(
                    component.Component(leftNode, rightNode,
                                        rigidLength,
                                        comp.find('name').text.strip(),
                                        False))
            # if instead it's a cross component
            else:
                # get first loadpath
                loadpath, = [loadpath for loadpath in struct.listLoadpaths
                             if loadpath.level == level_id]
                # get leftNode
                leftNode, = [node for node in loadpath.setNodes
                             if node.position == float(comp.
                                                       find('x1').text)]
                # get second loadpath
                level_id2 = int(comp.find('end_level').text)
                loadpath, = [loadpath for loadpath in struct.listLoadpaths
                             if loadpath.level == level_id2]
                # get rightNode
                rightNode, = [node for node in loadpath.setNodes
                              if node.position == float(comp.
                                                        find('x2').text)]
                if rightNode.position < leftNode.position:
                    leftNode, rightNode = rightNode, leftNode
                # compute rigid length
                length = rightNode.position - leftNode.position
                rigidLength = length - float(comp.find('defoLength').text)
                # create and append component
                struct.listCrossComponents.append(
                    cross_component.
                    CrossComponent(comp.find('name').text.strip(),
                                   leftNode, rightNode,
                                   rigidLength))
def gaps_insertor(structure):
    """Add gaps to the structure.

    Every gap is added (as a component) to the correct loadpath defined in
    struct.listLoadpaths. The loadpath must already contain all the nodes and
    all the components.
    Gaps are added where needed:
    – in front of loadpaths that are not directly connected to the barrier
    - between non-adjacent components
    - behind loadpaths that are not directly connected to the firewall

            gap                 gap                 gap
    |xx|            o-----o            o-----o            |x|
     
    barrier                                               firewall
    
    Args:
      struct:
        the structure_core.structure.Structure obj
    Returns:
      nothing is returned.
    Raises:
      nothing is raised.
    """
    leftLimit = min(component.leftNode.position
                    for loadpath in structure.listLoadpaths
                    for component in loadpath.listComponents)
    
    for loadpath in structure.listLoadpaths:
###############################################################################
        # add gaps in front of the loadpath
        node = min((node
                    for node in loadpath.setNodes),
                   key = lambda node: node.position)
        if leftLimit < node.position:
            frontNode = node.Node(leftLimit,             # position
                                  node.loadpathLevel)    # loadpath level
            
            gap = component. \
                  Component(frontNode,
                            node,
                            0,
                            'front-gap-{0}'.format(node.loadpathLevel),
                            True)
            loadpath.listComponents.append(gap)
            structure.listGaps.append(gap)
###############################################################################
        # add gaps between components
        # create a gap_name iterator (e.g. 'gap-0-1', 'gap-0-2', ...)
        name = gap_name(loadpath.level)
        # create and sort a list of nodes 
        listNodes = list(loadpath.setNodes)
        listNodes.sort(key = lambda node: node.position)
        # create two iterators
        nodes, next_nodes = tee(listNodes)
        # advance by one in next_nodes
        ignore_me = next(next_nodes)
        for node, next_node in zip(nodes, next_nodes):
            try:
                # look for a comp that goes from node to next_node
                comp, = [comp
                         for comp in loadpath.listComponents
                         if comp.leftNode is node
                         and comp.rightNode is next_node]
            except ValueError:
                # such a component doesn't exist
                # create a gap
                gap = component.Component(node, next_node, 0,
                                          next(name),
                                          True)
                loadpath.listComponents.append(gap)
                structure.listGaps.append(gap)

###############################################################################
        # add gaps behind the loadpath
        node = max((node
                    for node in loadpath.setNodes),
                   key = lambda node: node.position)
        if node.towardsFirewall:
            # there is at least a cross component going from the node towards
            # the firewall, thus a gap should be inserted

            # get all the loadpath linked to the right of the node 
            lp_levels = [crossComp.rightNode.loadpathLevel
                         for crossComp in node.towardsFirewall]
            # compute the rightLimit
            rightLimit = max(comp.rightNode.position
                             for lp in structure.listLoadpaths
                             if lp.level in lp_levels
                             for comp in lp.listComponents)
            backNode = node.Node(rightLimit,
                                 node.loadpathLevel)

            gap = component.\
                  Component(node,
                            backNode,
                            0,
                            "back-gap-{0}".format(node.loadpathLevel),
                            True)
            loadpath.listComponents.append(gap)
            structure.listGaps.append(gap)
###############################################################################

def gap_name(level):
    """Yields a string, to be used as a name for the next gap.

    Args:
      level:
        an integer, the level of the loadpath to which the gap belongs.
    Returns:
      a string
    Raises:
      nothing is raised.
    """
    counter = 0
    while True:
        yield 'gap-{0}{1}'.format(level, counter)
        counter += 1

def init_firewall_and_barrier(structure):
    """Initialise the connections of components, cross components and nodes.

    The attributes .connectedToBarrier and .connectedToFirewall of every
    structure_core.Component and structure_core.CrossComponent object are
    initialised.
    The attributes .onBarrier and .onFirewall of every structure_core.Node
    object are initialised.

    Args:
        structure:
            structure_core.structure.Structure object that groups components,
            cross components and nodes to initialise.
    Returns:
        nothing is returned.
    Raises:
        nothing is raised.
    """
    for loadpath in structure.listLoadpaths:
        frontNode = min((comp.leftNode
                         for comp in loadpath.listComponents),
                        key = lambda node: node.position)
        backNode = max((comp.rightNode
                        for comp in loadpath.listComponents),
                       key = lambda node: node.position)

        frontNode.onBarrier = True
        backNode.onFirewall = True

        for comp in frontNode.towardsFirewall:
            comp.link_to_barrier()
        for comp in backNode.towardsBarrier:
            comp.link_to_firewall()
