# import modules
import xml.etree.ElementTree as et
import structure
import loadpath as lp
import connectionpath as cp
import component as c
import node as nd

def read_xml(path = '/Users/massimosferza/LRZ Sync+Share/TUM/TUM SoSe16/Courses/Software Lab/Git_repository/no-block-example.xml'):
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
            for node in loadpath_obj.node_list:
                if x_position == node.x_position:
                    break
                else:
                    # if not add it
                    loadpath_obj.node_list.append(nd.Node(x_position))

            # for every component, that is not a connection
            if not 'X' in component.find('name').text:
                # get also x2
                x_position = float(component.find('x2').text)

                # and again
                # check if the loadpath already contains a node corresponding to
                # x2
                for node in loadpath_obj.node_list:
                    if x_position == node.x_position:
                        break
                    else:
                        # if not add it
                        loadpath_obj.node_list.append(nd.Node(x_position))

        print(node.x_position for node in loadpath_obj.node_list)
        #############################################################
        # add members to each loadpath
        for component in level.iter('component'):
            # for every component, that is not a connection
            if not 'X' in component.find('name').text:

                # get the previously created nodes
                x1 = float(component.find('x1').text)
                x2 = float(component.find('x2').text)
                for node in loadpath_obj.node_list:
                    if x1 == node.x_position:
                        node1 = node
                    if x2 == node.x_position:
                        node2 = node

                # create a member
                member_obj = c.Component(
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
    # collect all the connections in the following list
    connections = [ ]

    # create all the missing nodes, save them in a list such as
    # [[implicitly_defined_lp_id, node_object], [ , ], ...]
    free_nodes = [ ]
    for level in root.iter('level'):
        for component in level.iter('component'):
            if 'X' in component.find('name').text:
                # found a connection, check if its nodes already exist:
                    # the first node already exists for sure, since the loadpath
                    # object has been created and the first node was added in
                    # its node_list

                    # the second node EITHER belongs to another loadpath (and
                    # therefore it already exist) OR has to be created

                # get the loadpath id of the second node
                comp_name = component.find('name').text
                loadpath_id = comp_name.lstrip('X')
                second_lp_id = int(loadpath_id[1])

                # check if the loadpath already exists
                for path in new_structure.path_list:
                    if type(path) is lp.Loadpath
                    and path.id == second_lp_id:
                        # loadpath of the second node found
                        loadpath_obj = path
                try:
                    if loadpath_obj:
                        # the second node belongs to a loadpath and already
                        # exists
                        pass

                except NameError:
                    # the second node has to be created
                    pass

    # create all the connetion and save them in ...
    # split them in connectionpaths
    
    # divide the temporary list in connectionpaths
    while connections:
        connection_obj = connections.pop()

        # create a connectionpath
        connectionpath_obj = cp.Connectionpath()
        
         # add connection_obj to connectionpath_obj
        connectionpath_obj.component_list.append(connection_obj)

        # look for other connection that belong to the same connectionpath
        for connection_obj in connectionpath_obj:
            for connection in connections:
                if connection_obj.right_node == connection.left_node:
                    connectionpath_obj.component_list.append(connection)

        # add the connectionpath to the structure
        new_structure.path_list.append(connectionpath_obj)

#############################################################
    return new_structure

if __name__ == "__main__":
    struct = read_xml()
    for path in struct.path_list:
        if type(path) is lp.Loadpath:
            if not path.component_list:
                print("Loadpath", path.id, "is empty")
            else:
                print("Loadpath", path.id, "has these components:")
                for comp in path.component_list:
                    comp.print_info("\t")

        elif type(path) is cp.Connectionpath:
            print("A connectionpath has been created with these components:")
            for comp in path.component_list:
                comp.print_info("\t")


