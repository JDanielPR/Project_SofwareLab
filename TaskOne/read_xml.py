import xml.etree.ElementTree as et
from Structure import Structure
from Loadpath import Loadpath
from Component import Component
from CrossComponent import CrossComponent
from Node import Node

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

    # initialize the right components
    struct.init_right_components()

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
            if component.find('end_level'):
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
                    loadpathLevel = loadpath.listOfComponents[0].\
                                    leftNode.loadpathLevel
                    
                    if loadpathLevel == loadpathLevel1:
                        # loadpath 1 found
                        # loop over components:
                        for comp in loadpath.listOfComponents:
                            if comp.leftNode.position == x1:
                                left_node = comp.leftNode
                            elif comp.rightNode.position == x1:
                                left_node = comp.leftNode
                                
                    elif loadpathLevel == loadpathLevel2:
                        # loadpath 2 found
                        # loop over components:
                        for comp in loadpath.listOfComponents:
                            if comp.leftNode.position == x2:
                                right_node = comp.leftNode
                            elif comp.rightNode.position == x2:
                                right_node = comp.rightNode

                # ensure that the nodes have been found
                assert left_node
                assert right_node

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
                cross_comp_obj = CrossComponent(left_node, right_node,
                                                rigid_length)

                # save crossComponent
                listCrossComponents.append(cross_comp_obj)

    return listCrossComponents

