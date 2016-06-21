from . import component as c

class Connection(c.Component):
    def __init__(self, name,
                 node1, node2,
                 deformable_length, deformable_ratio):
        c.Component.__init__(self, name,
                             node1, node2,
                             deformable_length, deformable_ratio)
        
    def say_hi_to(self, infos_collector, node):
        if node == self.left_node:
            infos_collector.left_node_connection_list.append(self)
            
        elif node == self.right_node:
            infos_collector.right_node_connection_list.append(self)

        else:
            raise Exception(
                "In connection.py: say_hi_to(): this should never happen")
                            

