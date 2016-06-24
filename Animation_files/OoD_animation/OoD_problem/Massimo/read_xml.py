# import modules
import xml.etree.ElementTree as et
from . import structure
from . import loadpath as lp
from . import connectionpath as cp
#import component as c
from . import member as m
from . import connection as con
from . import node as nd

def read_xml(path ='C:\\FAPSA18\\JDPR\\TUM\\Second_Semester\\Sofware_Lab\\BMW\\Animation_files\\OoD_animation\\OoD_problem\\Massimo\\xml_files\\2_2_rd.xml'):
    """It creates a structure object for the OoD problem to solve, given a
proper .xml file"""

    # create a tree object, given the correct address of the .xml file
    tree = et.parse(path)

    # create a variable that contains the root
    root = tree.getroot()

#############################################################
    # create a structure
    new_structure = structure.Structure()

#############################################################
    # create all the loadpaths
    # loop over the element <level> </level> contained in root
    for level in root.iter('level'):
        
        # create a loadpath
        level_id = int(level.find('id').text)
        loadpath_obj = lp.Loadpath(level_id)
        
        #############################################################
        # add nodes to each loadpath
        for component in level.iter('component'):
            # for every component in the level, get x1 
            x_position = float(component.find('x1').text)

            # check if the loadpath already contains a node corresponding to x1
            already_contained = False
            for node in loadpath_obj.node_list:
                if x_position == node.x_position:
                    already_contained = True
                    break
            if not already_contained:
                # if not add it
                loadpath_obj.node_list.append(nd.Node(x_position))

            # for every component, that is not a connection
            if not is_a_connection(component):
                # get also x2
                x_position = float(component.find('x2').text)

                # and again
                # check if the loadpath already contains a node corresponding to
                # x2
                already_contained = False
                for node in loadpath_obj.node_list:
                    if x_position == node.x_position:
                        already_contained = True
                        break
                if not already_contained:
                    # if not add it
                    loadpath_obj.node_list.append(nd.Node(x_position))

        #############################################################
        # add members to each loadpath
        for component in level.iter('component'):
            # for every component, that is not a connection
            if not is_a_connection(component):

                # get the previously created nodes
                x1 = float(component.find('x1').text)
                x2 = float(component.find('x2').text)
                for node in loadpath_obj.node_list:
                    if x1 == node.x_position:
                        node1 = node
                    if x2 == node.x_position:
                        node2 = node

                # create a member
                member_obj = m.Member(
                    component.find('name').text,
                    node1,
                    node2,
                    float(component.find('defoLength').text),
                    float(component.find('defoRatio').text))

                # add the member to the loadpath
                loadpath_obj.component_list.append(member_obj)
            
        # add the loadpath to the structure
        new_structure.path_list.append(loadpath_obj)

#############################################################
    # create all the connectionpaths
    for level in root.iter('level'):
        for component in level.iter('component'):
            if is_a_connection(component):
                # found a connection
                # since the structure is simply connected
                # the nodes already exist in some loadpath node_list

                # get the id of the first and of the second loadpath,
                first_lp_id = int(level.find('id').text)
                second_lp_id = int(component.find('end_level').text)
                
                # get x1 and x2
                x1 = float(component.find('x1').text)
                x2 = float(component.find('x2').text)
                
                # get node 1 and node 2
                # initialize node1 and node2
                node1, node2 = None, None
                # loop over loadpaths and find the one with first_lp_id
                for path in new_structure.path_list:
                    if type(path) is lp.Loadpath:
                        if path.id == first_lp_id:
                            # found first loadpath
                            # loop over the nodes and find the one with x1 pos
                            for node in path.node_list:
                                if node.x_position == x1:
                                    # found first node
                                    node1 = node
                            # check if the node was found
                            if not node1:
                                # no matching node found
                                # invalid input file
                                name = component.find('name').text.strip()
                                raise Exception(
                                    "Invalid .xml: %s is not properly defined"
                                    %name)
                            
                        elif path.id == second_lp_id:
                            # found second loadpath
                            # loop over the nodes and find the one with x2 pos
                            for node in path.node_list:
                                if node.x_position == x2:
                                    # found second node
                                    node2 = node
                            # check if the node was found
                            if not node2:
                                # no matching node found
                                # invalid input file
                                name = component.find('name').text.strip()
                                raise Exception(
                                    "Invalid .xml: %s is not properly defined"
                                    %name)
                # check existance of node1 and node2
                if not node1 or not node2:
                    name = component.find('name').text.strip()
                    raise Exception("Invalid .xml: %s is not properly defined"
                                    %name)
                # create a connection
                connection_obj = con.Connection(
                    component.find('name').text,
                    node1,
                    node2,
                    float(component.find('defoLength').text),
                    float(component.find('defoRatio').text))

                # create a connectionpath
                connectionpath_obj = cp.Connectionpath()
                
                # add connection_obj to connectionpath_obj
                connectionpath_obj.component_list.append(connection_obj)

                # add the connectionpath to the structure
                new_structure.path_list.append(connectionpath_obj)

#############################################################
    # sort all the components by left node position
    # look for neighbours
    for [n, path] in enumerate(new_structure.path_list):
        path.sort_components()
        path.update_lp_level_of_isdh_components(n)
        path.compute_neighbours()

    # register all the isdh.components to the SolutionCollector
    new_structure.register_components()

    return new_structure

def is_a_connection(component):
    if component.find('end_level') is None:
        # it is not a connection
        return False
    else:
        # it is a connection
        return True

if __name__ == "__main__":
    struct = read_xml("xml_files/2_2_c1.xml")
    struct.print_read_data()


