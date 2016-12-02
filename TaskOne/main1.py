import pkg.tree_core
from pkg.structure_core.structure import Structure
from pkg.read_xml import read_xml
import pkg.GapsHandeling
from math import factorial

# read input
struct = read_xml('/Users/massimosferza/Desktop/benchmark.xml')

# solve
import time
start = time.time()
[i_s, d_h] = struct.task_one()
end = time.time()

# message
print("\nSolved in {0}s".format(end - start))
sol_found = len(d_h) # valid solutions found
precomp_sol = 1 # max number of possible solutions
for lp in struct.listLoadpaths:
    precomp_sol *= factorial(len(lp.listComponents))
message = "{0} valid solutions found out of {1} \
theoretically possible solutions"
print(message.format(sol_found, precomp_sol))
