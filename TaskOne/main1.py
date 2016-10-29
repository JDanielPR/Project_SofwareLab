import pkg.tree_core
from pkg.structure_core.Structure import Structure
from pkg.read_xml import read_xml
import pkg.GapsHandeling


##struct = read_xml('/Users/massimosferza/Desktop/test3.xml')
struct = read_xml('/Users/massimosferza/Desktop/2_2_c1.xml')
pkg.GapsHandeling.gapsInsertor(struct.listLoadpaths)

[i_s, d_h] = struct.task_one()
