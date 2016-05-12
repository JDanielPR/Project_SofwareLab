from read_xml import read_xml

# create a structure reading the input data
struct = read_xml()

# solve each path independently
for path in struct.path_list:
    path.solve()
    # now path.solution_list is a list created from an itertools.permutations
    # object,  which is an iterator:
    # each member of this iterator is a possible solution
    
    # each solution is a tuple object, which contains objects of type
    # component.Component

    print("solution of path", path.id, ":")
    print(path.path_solution_string(), "\n")

# combine the path solution to get the structure solution 
