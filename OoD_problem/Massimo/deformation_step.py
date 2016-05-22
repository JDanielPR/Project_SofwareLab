class DeformationStep:
    """Infos collector: this class collects infos about the upcoming
deformation step."""
    def __init__(self):
        max_deformation = None
        left_node_connection_list = [ ]
        right_node_connection_list = [ ]

    def test(self):
        """Returns a True if the deformation step is valid, else False."""
# when moving a connection there might be 3 cases:
#               <--/        |   <--/         |        /
#                 /  case 1 |     /   case2  |       /    case 3
#             <--/          |    /           |   <--/
#
# case 1 left and right node are moved: the connection is translated
#   always possible    
#
# case 2 right node is moved: the connection becomes shorter
#   possible if the movement isn't bigger than the deformable length
#
# case 3 left node is moved: the connection becomes longer
#   impossible

        # structure of the function:
        #   1. look for a connection that becomes longer
        #       - if one is found: return False
        #   2. check if max_deformation is correct:
        #       - when the function is called the value of max_deformation
        #         is the minimum of the current_deformable_length among the
        #         the elements. It might be that a connection that deforms
        #         has a current_deformable_length smaller than max_deformation.
        #         In this case the value of max_deformation is changed
        #   3. the deformation makes sense and max_deformation is correct
        #       - return True

        # 1. look for a case 3
        # loop over all the connections in left_node_connection_list
        for connection in self.left_node_connection_list:

            # if they are also in right_node_connection_list
                # case 1: no problem

            # else
            if not connection in self.right_node_connection_list:
                # case 3: the deformation step is impossible
                # the solution does not make sense
                return False
            
        # 2. correct max_deformation
        # loop over all the connections that belong to case 2
        for connection in self.right_node_connection_list:
            if not connection in self.left_node_connection_list:
                # case 2
                if connection.current_deformable_length < self.max_deformation:
                    # if the value of max deformation is too big, change it
                    self.max_deformation = connection.current_deformable_length

        # 3. return
        return True
                

    def re_init(self):
        self.max_deformation = None
        self.left_node_connection_list = [ ]
        self.right_node_connection_list = [ ]
