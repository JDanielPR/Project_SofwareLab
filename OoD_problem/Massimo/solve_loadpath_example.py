"""
This script is to demonstrate how powerful is the itertool module, which allows
python to compute combinations and similar staff.
It's really convenient for our problem

example:
I'm considering the following structure, made of 2 loadpaths in parallel.
Each loadpath has 3 members

LEGEND:
    ---- deformable lenght
    ==== rigid length
    o    node
    
############################################

        o------==o---=====o----=o
        member1   member2  member3

        o---===o---=o-------====o
       member4 member5 member6

############################################

by Massimo Sferza
"""

# import a really cool py module
import itertools

# define each path as a list of members
list_of_members1 = ["member1", "member2", "member3"]
list_of_members2 = ["member4", "member5", "member6"]

# compute the solution of each loadpath independently
loadpath1_solution = itertools.permutations(list_of_members1)
loadpath2_solution = itertools.permutations(list_of_members2)

# compute the global solution as the product set of the two loadpath solutions
structure_solution = itertools.product(loadpath1_solution, loadpath2_solution)

# print the result to see what happened
for i in structure_solution:
    print(i)
