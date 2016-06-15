import member
import loadpath
import copy
import logging

logger = logging.getLogger('nextstep')
logging.basicConfig(level=logging.DEBUG)

class nextstep():

  #initialization of the created object
  def __init__(self, etree, history, pstep):

    #input tree for this object to start from
    self.elementTree = etree

    logger.debug("steped into another level has {} possibilities".format(len(self.elementTree)))
                                                                    
    #list of trees results from the motion undertaken by each tuple of the input tree for this object
    self.nStepsGroup = []

    #(START)stores the previously performed steps that led to the current tree of possibilities
    if history == None:
      self.path = []
    else:
      self.path = copy.deepcopy(history)
    #(END)stores the previously performed steps that led to the current tree of possibilities

    #(START)append the step resulted this breanch of possibilities into "path"
    if pstep != None:
      self.path.append(pstep)
    #(END)append the step resulted this breanch of possibilities into "path"

    self.carryon()
    
    
  #responsible function for performing the procedure of elemination of the impossible happining sequences "tuples"
  def treeTailoring(self, localtree):

    #(START)tailoring process
    domain = len(localtree)
    c = 0
    for i in range(0,domain):
      print(len(localtree))
      for j in localtree[i-c]:
        if j.state == False:
          localtree.remove(localtree[i-c])
          c = c+1
          break
    #(END)tailoring process

    logger.debug("a tree has been toilored to {} possibilities".format(len(localtree)))

    #(START)print out the possbile sequences
    for i in localtree:
      for j in i:
        print(j.name)
    #(END)print out the possible sequences
        
    return(localtree)

  #resposible function for perfoming the procedure of stepping
  def carryon(self):

    #this counter will be used to go over all the tuples in localtree(which is a copy of the passed elementtree to apply changes without affecting it)
    counter = 0

    #loop over all the branches of the passed OoD tree 
    for i in self.elementTree:
      
      #create a copy of the input tree to reserve it against any changes
      localtree = copy.deepcopy(self.elementTree)
      
    
      #(START)determining the motion to be carried out perform it 
      deformotion = 1111111
      for j in i:
        if j.dLength < deformotion:
          deformotion = j.dLength
      deformotion = round(deformotion,1)
      #(END)determining the motion to be carried out perform i
      

      #(START)determine whether the current branch is valid to lead the deformation
      decidor = 0
      for j in localtree[counter]:
        if j.deformPossibility == True:
          decidor = decidor +1
      #(END)determine whether the current branch is valid to lead the deformation
        

      #(START)if amount of deformation is not zero, AND the decidor agreed on deforming, then DEFORM!
      if deformotion != 0 and decidor == len(i):
        
        count = 0
        
        for j in localtree[counter]:

          j.deform(deformotion)
          logger.info("member {} has deformed by {}".format(j.name, deformotion))

          if j.calLength() == j.rigidLength:
            j.changeState(False)
            logger.info("a member has changed its state")
            j.canDeform(False)
            for k in localtree: #Switch all of the members along the loadpath containing member j on again
              if k[count].name != j.name:
                k[count].canDeform(True)
            
          else:
            j.canDeform(True) #member j will keep leading the deformation in its own loadpath
            logger.warning("a member has not reached its max. deformation")
            for k in localtree: #Switch all of the members along the loadpath containing member j off so they dont deform untill member j is done
              if k[count].name != j.name:
                k[count].canDeform(False)
                logger.warning("an element has been swteched off from leading the deformation temporarily")
                
          count = count + 1
      #(END)the deformation process
          

      #(START)add a new member to the list that contains all of the next steps resulting from the input step to this object
      if decidor == len(i):
        b = self.treeTailoring(localtree)
        if len(b) != 0:
          logger.debug("a new level of trees is created")
          self.nStepsGroup.append(nextstep(b,self.path,i))
      #(END)end of the process of crearing a new tree of the current branch

      #(START)SHOWING a found OoD
        else:
          print('one OoD is:')
          for x in self.path:
            for y in x:
              print(y.name)
            print('...........')
          for x in i:
            print(x.name)
          print('end of this found OoD!')   
      #(END)SHOWING a found OoD


      counter = counter +1 #increment the counter by one to go to the next tuple
  



