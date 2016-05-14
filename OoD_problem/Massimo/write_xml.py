from xml.etree.ElementTree import *
from xml.dom import minidom

def create_level(root, index):
    level = SubElement(root,'level')
    id_n = SubElement(level,'id')
    id_n.text = str(index)
    return level

def create_component(level, input_name, input_x1, input_x2, input_defoLength):

    component = SubElement(level, 'component')

    name = SubElement(component, 'name')
    x1 = SubElement(component, 'x1')
    x2 = SubElement(component, 'x2')
    defoLength = SubElement(component, 'defoLength')
    defoRatio = SubElement(component, 'defoRatio')

    name.text = input_name
    x1.text = input_x1
    x2.text = input_x2
    defoLength.text = input_defoLength
    defoRatio.text = str(int(input_defoLength) / (int(input_x2) - int(input_x1)))

def ask_for_new_level(root):
    index = 0
    y_n = 'y'
    while y_n != 'n':  
        y_n = input("do you want to add a loadpath?\t")
        if y_n == 'y':
            level = create_level(root, index)
            ask_for_new_component(level, index)
            index += 1

def ask_for_new_component(level, lp_i):
    cp_i = 0
    y_n = 'y'
    while y_n != 'n':  
        y_n = input("do you want to add a component?\t")
        if y_n == 'y':
            input_name = "e" + str(lp_i) + str(cp_i)
            input_x1 = input("insert x1\t")
            input_x2 = input("insert x2\t")

            message = "the current length is: "
            message += str(int(input_x2) - int(input_x1))
            message += "\ninsert the deformable length\t"
            input_defoLength = input(message)
            create_component(level,
                             input_name,
                             input_x1,
                             input_x2,
                             input_defoLength)
            cp_i += 1
            


root = Element('root')
ask_for_new_level(root)
tree = ElementTree(root)
tree.write("output.xml")

        
