import member as mem

class nextstep():
  
  def __int__(self,etree):
    self.elementtree = etree

  def treetailoring(self):
    for i in len(elementtree):
      for j in range(len(elementtree[i])):
        if elementtree[i][j] == False:
          elementtree.pop(i)
          

  def carryon(self):

    for i in elementtree:

      counter = 0
    
      #determining the motion to be carried out perform it
      deformotion = 1111111
      for j in range(2):
        if i[j].dlength < deformotion:
          deformotion = i[j].dlength
      print(deformotion)

      #perform the deformation upon the elements and change the position and state of all the elements
      for j in range(2):
        i[j].deform(deformotion)
        print(i[j].calLength())
        if i[j].calLength() <= (i[j].length-i[j].dlength):
          i[j].changestate(False)
        print(i[j].state)

      ns1 = nextstep.nextstep(self.elementtree)
      ns1.treetailoring()
      ns1.caryon()

    
