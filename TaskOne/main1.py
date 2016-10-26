import pkg.tree_core
from pkg.structure_core.Structure import Structure
from pkg.read_xml import read_xml
import pkg.GapsHandeling


struct = read_xml('/Users/massimosferza/Desktop/test3.xml')
pkg.GapsHandeling.gapsInsertor(struct.listLoadpaths)

tree = struct.possibilities_tree_generator()

tree.deform()
tree.add_children()
while not tree.end:
    tree.go_down()
    tree.deform()
    tree.add_children()
    
tree.go_up()
