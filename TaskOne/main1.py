import pkg.tree_core
from pkg.structure_core.Structure import Structure
from pkg.read_xml import read_xml
import pkg.GapsHandeling

#### needed for testing
##from pkg.tree_core.tree import Tree


struct = read_xml('/Users/massimosferza/Desktop/no-block-example.xml')

[i_s, d_h] = struct.task_one()

#### testing
##tree = Tree(struct)
##tree.add_children()
