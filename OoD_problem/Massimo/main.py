from read_xml import read_xml
from time import clock
# create a structure reading the input data
struct = read_xml("xml_files/2_2_c1.xml")

t1 = clock()

# solve it
struct.solve()

t2 = clock()
print("Total time running struct.solve: %s seconds" % str(t2-t1))

# output the solution
struct.print_solution()
