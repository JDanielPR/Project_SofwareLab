import xml.etree.ElementTree as et
from .structure_core import Structure
from .structure_core import Loadpath2
from .structure_core import Component
from .structure_core import CrossComponent
from .structure_core import Node
from itertools import tee

def read_xml(path):
    """Return a Structure object, based on the .xml at the given path"""
    # create a tree object, given the address of the .xml file
    tree = et.parse(path)
    # create a variable that contains the root
    root = tree.getroot()
    # create empty structure
    struct = Structure.Structure([ ],[ ])
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
    # loop over levels (i.e. loadpath levels)
    for level in root.iter('level'):
        # create a loadpath
        level_id = int(level.find('id').text)
        loadpath = Loadpath2.Loadpath(level_id)
        # loop over components to add nodes
        for component in level.iter('component'):
            if component.find('end_level') is None: # skip crossComponents
                x = float(component.find('x1').text)
                loadpath.setNodes.add(Node.Node(x, level_id))
                x = float(component.find('x2').text)        
                loadpath.setNodes.add(Node.Node(x, level_id))
        # append loadpath
        if loadpath.setNodes:
            struct.listLoadpaths.append(loadpath)
    # loop over cross components
    for component in root.iter('component'):
        if component.find('end_level') is not None:
            # look for loadpaths defined implicitly by "end_level" 
            level_id = int(component.find('end_level').text)
            try:
                loadpath, = [loadpath for loadpath in struct.listLoadpaths
                             if loadpath.level == level_id]
            except ValueError:
                # no such a loadpath, create it
                loadpath = Loadpath2.Loadpath(level_id)
                # append loadpath
                struct.listLoadpaths.append(loadpath)
            # add node
            x = float(component.find('x2').text)
            loadpath.setNodes.add(Node.Node(x, level_id))

def add_components(root, struct):
    # loop over components
    for level in root.iter('level'):
        level_id = int(level.find('id').text)
        for component in level.iter('component'):
            # if it's a normal component
            if component.find('end_level') is None:
                # get loadpath
                loadpath, = [loadpath for loadpath in struct.listLoadpaths
                             if loadpath.level == level_id]
                # get nodes
                leftNode, = [node for node in loadpath.setNodes
                             if node.position == float(component.
                                                       find('x1').text)]
                rightNode, = [node for node in loadpath.setNodes
                              if node.position == float(component.
                                                        find('x2').text)]
                if rightNode.position < leftNode.position:
                    leftNode, rightNode = rightNode, leftNode
                # compute rigid length
                length = rightNode.position - leftNode.position
                rigidLength = length - float(component.find('defoLength').text)
                # create and append component
                loadpath.listComponents.append(
                    Component.Component(leftNode, rightNode,
                                        rigidLength,
                                        component.find('name').text.strip(),
                                        False))
            # if instead it's a cross component
            else:
                # get first loadpath
                loadpath, = [loadpath for loadpath in struct.listLoadpaths
                             if loadpath.level == level_id]
                # get leftNode
                leftNode, = [node for node in loadpath.setNodes
                             if node.position == float(component.
                                                       find('x1').text)]
                # get second loadpath
                level_id2 = int(component.find('end_level').text)
                loadpath, = [loadpath for loadpath in struct.listLoadpaths
                             if loadpath.level == level_id2]
                # get rightNode
                rightNode, = [node for node in loadpath.setNodes
                              if node.position == float(component.
                                                        find('x2').text)]
                if rightNode.position < leftNode.position:
                    leftNode, rightNode = rightNode, leftNode
                # compute rigid length
                length = rightNode.position - leftNode.position
                rigidLength = length - float(component.find('defoLength').text)
                # create and append component
                struct.listCrossComponents.append(
                    CrossComponent.
                    CrossComponent(component.find('name').text.strip(),
                                   leftNode, rightNode,
                                   rigidLength))
def gaps_insertor(structure):
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
            frontNode = Node.Node(leftLimit,             # position
                                  node.loadpathLevel)    # loadpath level
            
            gap = Component. \
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
                gap = Component.Component(node, next_node, 0,
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
            backNode = Node.Node(rightLimit,
                                 node.loadpathLevel)

            gap = Component.\
                  Component(node,
                            backNode,
                            0,
                            "back-gap-{0}".format(node.loadpathLevel),
                            True)
            loadpath.listComponents.append(gap)
            structure.listGaps.append(gap)
###############################################################################

def gap_name(level):
    counter = 0
    while True:
        yield 'gap-{0}{1}'.format(level, counter)
        counter += 1

def init_firewall_and_barrier(structure):
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
