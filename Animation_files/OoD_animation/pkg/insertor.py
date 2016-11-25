def gaps_insertor(structure):
    leftLimit = min(component.leftNode.position
                    for loadpath in structure.listLoadpaths
                    for component in loadpath.listComponents)
    
    for loadpath in structure.listLoadpaths:
        # create a temporary list for gaps
        tmp = [ ]
###############################################################################
        # add gaps in front of the loadpath
        node = min(component.leftNode
                   for component in loadpath.listComponents,
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
        node = max(component.rightNode
                   for component in loadpath.listComponents,
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
        # sort the loadpath components by position of the left node
        loadpath.listComponents.sort(key = lambda comp: comp.leftNode.position)

def gap_name(level):
    counter = 0
    while True:
        yield 'gap-{0}-{1}'.format(level, counter)
        counter += 1
