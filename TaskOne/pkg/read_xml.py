import xml.etree.ElementTree as et
from .structure_core.Structure import Structure
from .structure_core.Loadpath import Loadpath
from .structure_core.Component import Component
from .structure_core.CrossComponent import CrossComponent
from .structure_core.Node import Node
from itertools import tee

def read_xml(path):
    """Return a Structure object, based on the .xml at the given path"""

    # create a tree object, given the address of the .xml file
    tree = et.parse(path)
    # create a variable that contains the root
    root = tree.getroot()

    # create the listLoadpaths
    listLoadpaths = construct_loadpaths(root)
    
    # create the listCrossComponents 
    listCrossComponents = construct_cross_components(root, listLoadpaths)

    # create the Structure object
    struct = Structure(listLoadpaths, listCrossComponents)

    # insert gaps
    gaps_insertor(struct)
    
    # initialise firewall and barrier
    init_firewall_and_barrier(struct)

    return struct

def construct_loadpaths(root):
    """Return a list of Loadpath objects, given the root of the .xml tree"""

    # create an empty list
    listLoadpaths = [ ]
    
    # loop over the element <level> </level> contained in root
    for level in root.iter('level'):
        # create a loadpath
        level_id = int(level.find('id').text)
        loadpath = Loadpath()

        # fill the loadpath
        # collect nodes
        nodes = set()
        # loop over components
        for component in level.iter('component'):
            if component.find('end_level') is None: # skip crossComponents
                x = float(component.find('x1').text)
                nodes.add(Node(x, level_id))
                x = float(component.find('x2').text)        
                nodes.add(Node(x, level_id))

        # loop over components
        for component in level.iter('component'):
            # skip crossComponents
            if component.find('end_level') is None:
                # get the previously created nodes
                x1 = float(component.find('x1').text)
                x2 = float(component.find('x2').text)
                for node in nodes:
                    if x1 == node.position:
                        node1 = node
                    if x2 == node.position:
                        node2 = node

                # check proper orientation of the Component
                if node1.position < node2.position:
                    pass # this should be the case, if the .xml is correct 
                else:
                    # in this case, swap the nodes
                    node1, node2 = node2, node1

                # calculate rigid length
                length = abs(x1 - x2)
                rigidLength = length - float(component.find('defoLength').text)
                # create component
                comp_obj = Component(node1, node2,
                                     rigidLength,
                                     component.find('name').text.strip())
                # save component
                loadpath.add_member(comp_obj)        

        # save the loadpath
        listLoadpaths.append(loadpath)

    return listLoadpaths

def construct_cross_components(root, listLoadpaths):
    """Return a list of crossComponent objects, given the root of the .xml
tree and the list of loadpaths."""

    # create an empty list
    listCrossComponents = [ ]

    # loop over the element <level> </level> contained in root
    for level in root.iter('level'):
        # loop over crossComponents
        for component in level.iter('component'):
            print("I'm in")
            if component.find('end_level') is not None:
                # read the position of the nodes
                x1 = float(component.find('x1').text)
                x2 = float(component.find('x2').text)
                # read the loadpath of the nodes
                loadpathLevel1 = int(level.find('id').text)
                loadpathLevel2 = int(component.find('end_level').text)
                # look for the nodes:
                left_node = None
                right_node = None
                # loop over the loadpaths
                for loadpath in listLoadpaths:
                    # get loadpathLevel
                    try:
                        loadpathLevel = loadpath.listComponents[0].\
                                        leftNode.loadpathLevel
                        if loadpathLevel == loadpathLevel1:
                            # loadpath 1 found
                            # loop over components:
                            for comp in loadpath.listComponents:
                                if comp.leftNode.position == x1:
                                    left_node = comp.leftNode
                                elif comp.rightNode.position == x1:
                                    left_node = comp.leftNode
                                    
                        elif loadpathLevel == loadpathLevel2:
                            # loadpath 2 found
                            # loop over components:
                            for comp in loadpath.listComponents:
                                if comp.leftNode.position == x2:
                                    right_node = comp.leftNode
                                elif comp.rightNode.position == x2:
                                    right_node = comp.rightNode
                    except IndexError:
                        # the loadpath is empty
                        pass


                # ensure that the nodes have been found
                try:
                    assert left_node
                except AssertionError:
                    raise Exception("Unable to find left node of {0}"
                                    .format(component.find('name')
                                            .text.strip()))
                try:
                    assert right_node
                except AssertionError:
                    raise Exception("Unable to find right node of {0}"
                                    .format(component.find('name')
                                            .text.strip()))

                # check proper orientation of the crossComponent
                if left_node.position < right_node.position:
                    pass # this should be the case, if the .xml is correct 
                else:
                    # in this case, swap the nodes
                    left_node, right_node = right_node, left_node

                # calculate rigid length
                length = abs(x1 - x2)
                rigidLength = length - float(component.find('defoLength').text)
                assert rigidLength >= 0
                
                # create crossComponent
                cross_comp_obj = CrossComponent(component.find('name').
                                                text.strip(),
                                                left_node, right_node,
                                                rigidLength)

                # save crossComponent
                listCrossComponents.append(cross_comp_obj)
                print("I'm out")

    return listCrossComponents

def gaps_insertor(structure):
    leftLimit = min(component.leftNode.position
                    for loadpath in structure.listLoadpaths
                    for component in loadpath.listComponents)
    
    for loadpath in structure.listLoadpaths:
        # create a temporary list for gaps
        tmp = [ ]
###############################################################################
        # add gaps in front of the loadpath
        node = min((component.leftNode
                    for component in loadpath.listComponents),
                   key = lambda node: node.position)
        if leftLimit < node.position:
            frontNode = Node(leftLimit,             # position
                             node.loadpathLevel)    # loadpath level
            
            gap = Component(frontNode,
                            node,
                            0,
                            'front-gap-{0}'.format(node.loadpathLevel),
                            True)
            tmp.append(gap)
###############################################################################
        # add gaps between components
        # create a gap_name iterator (e.g. 'gap-0-1', 'gap-0-2', ...)
        name = gap_name(loadpath.listComponents[0].leftNode.loadpathLevel)

        # sort the loadpath components by position of the left node
        loadpath.listComponents.sort(key = lambda comp: comp.leftNode.position)

        # create two iterable
        components, next_components = tee(loadpath.listComponents)
        # make next_components advance by one
        ignore_me = next(next_components)
        for comp, next_comp in zip(components, next_components):
            if comp.rightNode is not next_comp.leftNode:
                gap = Component(comp.rightNode,     # left node
                                next_comp.leftNode, # right node
                                0,                  # rigid length
                                next(name),         # name
                                True)               # isGap
                tmp.append(gap)
###############################################################################
        # add gaps behind the loadpath
        node = max((component.rightNode
                    for component in loadpath.listComponents),
                   key = lambda node: node.position)
        if node.towardsFirewall:
            # there is at least a cross component going from the node towards
            # the firewall, thus a gap should be inserted

            # get all the loadpath linked to the right of the node 
            lp_levels = [crossComp.rightNode.loadpathLevel
                         for crossComp in node.towadsFireWall]
            # for each of them get its right limit
            rightLimits = [ ]
            for lp in structure.listLoadpaths:
                if lp.listComponents[0].leftNode.loadpathLevel in lp_levels:
                    rightLimits.append(max(comp.rightNode.position
                                           for comp in lp.listComponents))
            # take the maximum of all
            rightLimit = max(rightLimits)

            backNode = Node(rightLimit,
                            node.loadpathLevel)

            gap = Component(node,
                            backNode,
                            0,
                            next(name),
                            True)
            tmp.append(gap)
###############################################################################
        # add the created gaps
        loadpath.listComponents += tmp
        structure.listGaps += tmp
        # sort the loadpath components by position of the left node
        loadpath.listComponents.sort(key = lambda comp: comp.leftNode.position)

def gap_name(level):
    counter = 0
    while True:
        yield 'gap-{0}-{1}'.format(level, counter)
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
