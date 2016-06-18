print("/solver_module/module.py\tIMPORTED")

print("/solver_module/module.py:\t attempt to \
import /solver_module/other_module.py")
from . import other_module

def foo():
    print('foo() function, defined in solver_module/module.py has been called')
