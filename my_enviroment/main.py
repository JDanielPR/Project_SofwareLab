###################### TEST 1
print('/main.py:\t attempt to import module from solver_package')
from .solver_package import module

print('/main.py:\t attempt to call module.foo()')
module.foo()
"""
###################### TEST 2
import solver_package.module

###################### TEST 3
import solver_package.module as m
m.foo()

###################### TEST 4 FAILED
import solver_package
solver_package.module.foo()
## AttributeError: module 'solver_module' has no attribute 'module'

###################### TEST 5 FAILED
from solver_package import *
module.foo()
## NameError: name 'module' is not defined

###################### TEST 6 FAILED
from solver_package import *
solver_package.module.foo()
## NameError: name 'solver_module' is not defined

###################### TEST 7 FAILED
from solver_package import *
foo()
## NameError: name 'foo' is not defined
"""
def read_xml():
    print('hi')
