import member as mem
import loadpath as lp
import nextstep as ns
import itertools

#creating member objects (THIS CAN BE DONE AUTOMATICALLY)
m1 = mem.member(0,4,0.50,'L1E1',None)
m2 = mem.member(4,8,0.75,'L1E2',m1)
m5 = mem.member(8,10,0.25,'L1E3',m2)
m3 = mem.member(0,4,0.50,'L2E1',None)
m4 = mem.member(4,8,0.75,'L2E2',m3)
m6 = mem.member(8,10,0.50,'L2E3',m4)
m7 = mem.member(0,6,0.50,'L3E1',None)
m8 = mem.member(6,10,0.50,'L3E2',m7)

#organizing member objects in a single array (THIS CAN BE DONE AUTOMATICALLY)
lp1 = lp.loadpath(1)
lp2 = lp.loadpath(2)
lp3 = lp.loadpath(3)

lp1.addMember(m1)
lp1.addMember(m2)
lp1.addMember(m5)
lp2.addMember(m3)
lp2.addMember(m4)
lp2.addMember(m6)
lp3.addMember(m7)
lp3.addMember(m8)

loadpath = [[m1,m2,m5],[m3,m4,m6],[m7,m8]]

for i in loadpath:
  for j in i:
    print(j.calLength())
    print(j.leftnode,"",j.rightnode)

#create the tree of possibilities 
lpgroup = list(itertools.product(*loadpath))

#prints the motion possibilities
for i in lpgroup:
  for j in i:
    print(j.name)
print('\n')

nstep = ns.nextstep(lpgroup,None,None)

##ANOTHER STRUCTURE FOR THE TEST OF MEMBERS WITH GAPS
#m1 = mem.member(0,3,1.00,'GAP1',None)
#m2 = mem.member(3,7,0.75,'L1E1',m1)
#m3 = mem.member(7,11,0.25,'GAP2',m2)
#m4 = mem.member(11,13,0.50,'L1E3',m3)

#m5



  

  


