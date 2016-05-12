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
            already_contained = False
            for node in loadpath_obj.node_list:
                if x_position == node.x_position:
                    already_contained = True
                    break
            if not already_contained:
                # if not add it
                loadpath_obj.node_list.append(nd.Node(x_position))

            # for every component, that is not a connection
            if not 'X' in component.find('name').text:
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
    # neglect all the connectionpaths
#############################################################
    return new_structure

if __name__ == "__main__":
    struct = read_xml()
    if True:
        struct.path_list[2].solve()
        struct.path_list[2].print_solution_list()
    else:
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
