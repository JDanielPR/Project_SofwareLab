import member as mem
import nextstep as ns
import itertools

#creating member objects (THIS CAN BE DONE AUTOMATICALLY)
m1 = mem.member(0,3,0.7,'L1E1',None)
m2 = mem.member(3,5,0.7,'L1E2',m1)
m3 = mem.member(0,2,0.7,'L2E1',None)
m4 = mem.member(2,5,0.7,'L2E2',m3)

#organizing member objects in a single array (THIS CAN BE DONE AUTOMATICALLY)
loadpath = [[m1,m2],[m3,m4]]

for i in loadpath:
  for j in i:
    print(j.calLength())
    print(j.leftnode,"",j.rightnode)

#create the tree of possibilities 
lpgroup = list(itertools.product(*loadpath))

#prints the motion possibilities
for i in lpgroup:
  print('combination: ')
  for j in i:
    print(j.name)

#running over all of the possible starting sequences
for i in lpgroup:

  counter = 0
  
  #exit the loop for only one TEST cycle
  breaker = 1
  
  #determining the motion to be carried out perform it
  deformotion = 1111111
  for j in range(len(lpgroup[counter])):
    if i[j].dlength < deformotion:
      deformotion = i[j].dlength
  print(deformotion)

  #perform the deformation upon the elements and change the position and state of all the elements
  for j in range(len(lpgroup[counter])):
    i[j].deform(deformotion)
    print(i[j].calLength())
    if i[j].calLength() <= (i[j].length-i[j].dlength):
      i[j].changestate(False)
    print(i[j].state)

  

  

  counter += 1
  
  if breaker == 1:
    break
  

  

  


