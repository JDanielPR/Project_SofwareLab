"""
This script is an example of how to use the xml.etree.ElementTree module to
parse an .xml file

by Massimo Sferza
"""

# import the module
import xml.etree.ElementTree as et

# create a tree object, given the correct address of the .xml file
tree = et.parse('\
/Users/massimosferza/LRZ Sync+Share/TUM/TUM SoSe16\
/Courses/Software Lab/Git_repository/no-block-example.xml\
')

# an .xml has a tree structure:
# it has a root (e.g. geo_data in our case), which is an element
# the root has children, which are element too
# each child might have other children

# create a variable that contains the root
root = tree.getroot()

# loop over the element <component> </component> contained in root
for comp in root.iter('component'):
    # comp.find('name') finds the element <name> </name>
    # the .text method returns the string in the element
    print("\n\nfound a component with name: ", comp.find('name').text)
    print("the component has the following data:")

    # loop over the children of comp
    for data in comp:
        # the .tag method returns the tag of the children
        print("\t", data.tag, comp.find(data.tag).text)

