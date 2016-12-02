import pkg.tree_core
from pkg.structure_core.structure import Structure
from pkg.read_xml import read_xml
import pkg.GapsHandeling
##from pkg.isdh.isdh_helper import IsdhHelper

def blackbox(something):
    print('blackbox valid?')
    answer = input('y/n?\t')
    if answer == 'y':
        return True
    else:
        return False

struct = read_xml('/Users/massimosferza/Desktop/test3.xml')
pkg.GapsHandeling.gapsInsertor(struct.listLoadpaths)

[i_s, d_h] = struct.task_two(blackbox)
