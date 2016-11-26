import xml.etree.cElementTree as ET

tree = ET.ElementTree(file='no-block-example.xml')
root = tree.getroot()
print(root.tag)
print(root.attrib)
for child_of_root in root:
    print(child_of_root.tag)

for x in root.iter('level'):
    for comp in x.iter('component'):
        a = comp.find('name')
        print(a.text)
    
