import tree_core
from structure_core.Structure import Structure
from read_xml import read_xml
import GapsHandeling

def blackbox(something):
    answer = input('y/n?\t')
    if answer == 'y':
        return True
    else:
        return False

struct = read_xml('/Users/massimosferza/Desktop/test5.xml')
GapsHandeling.gapsInsertor(struct.listLoadpaths)

tree = struct.possibilities_tree_generator()
