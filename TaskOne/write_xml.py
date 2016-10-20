from xml.etree.ElementTree import *
from xml.dom import minidom
from math import fabs

def create_level(root, index):
    level = SubElement(root,'level')
    id_n = SubElement(level,'id')
    id_n.text = str(index)
    return level

def create_component(level,
                     input_name,
                     input_x1, input_x2,
                     input_defoLength,
                     input_end_lp = None):

    component = SubElement(level, 'component')

    name = SubElement(component, 'name')
    x1 = SubElement(component, 'x1')
    x2 = SubElement(component, 'x2')
    defoLength = SubElement(component, 'defoLength')
    defoRatio = SubElement(component, 'defoRatio')
    if input_end_lp:
        end_lp = SubElement(component, 'end_level')

    name.text = input_name
    x1.text = input_x1
    x2.text = input_x2
    defoLength.text = input_defoLength
    defoRatio.text = str(int(input_defoLength)
                         / fabs(int(input_x2) - int(input_x1)))
    if input_end_lp:
        end_lp.text = input_end_lp

def ask_for_new_level(root):
    index = 0
    y_n = 'y'
    while y_n != 'n':  
        y_n = input("do you want to add a loadpath?\t")
        if y_n == 'y':
            print('\nIn loadpath %i:\n' %index)
            level = create_level(root, index)
            ask_for_new_member(level, index)
            ask_for_new_connection(level, index)
            index += 1

def ask_for_new_member(level, lp_i):
    cp_i = 0
    y_n = 'y'
    while y_n != 'n':  
        y_n = input("do you want to add a member?\t")
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

def ask_for_new_connection(level, lp_i):
    y_n = 'y'
    while y_n != 'n':  
        y_n = input("do you want to add a connection? \t")
        if y_n == 'y':
            end_lp = input("to which loadpath would you like to connect?")
            input_name = "X" + str(lp_i) + str(end_lp)
            input_x1 = input("insert x1\t")
            input_x2 = input("insert x2\t")

            message = "the current length is: "
            message += str(fabs(int(input_x2) - int(input_x1)))
            message += "\ninsert the deformable length\t"
            input_defoLength = input(message)
            create_component(level,
                             input_name,
                             input_x1,
                             input_x2,
                             input_defoLength,
                             end_lp)

            
def prettify(path):
    xml = minidom.parse(path)
    prettyxml_str = xml.toprettyxml()
    output_file = open(path, 'w' )
    output_file.write(prettyxml_str)
    output_file.close()

def new_xml():
    root = Element('root')
    ask_for_new_level(root)
    tree = ElementTree(root)
    path = "/Users/massimosferza/Desktop/" + input("Insert file name: ") + ".xml"
    tree.write(path)
    prettify(path)
            




    
