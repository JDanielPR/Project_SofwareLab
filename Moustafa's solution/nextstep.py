import member
import loadpath
import copy
import logging
import gapsHandeling
import deformationCrossMembers 
import deformingFunction

logger = logging.getLogger('nextstep')
logging.basicConfig(level=logging.DEBUG)

class nextstep():

  #initialization of the created object
  def __init__(self, etree, history, pstep, listCrssMembs):

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

    self.listCrossMembers = listCrssMembs

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

    #counter for the times that the tree's branch has been skipped due to the violation of the assumptions related to cross members
    crossMembFailureCounter = 0

    #loop over all the branches of the passed OoD tree 
    for i in self.elementTree:
      
      #create a copy of the input tree to reserve it against any changes AND a copy of the list of cross members passed
      localtree = copy.deepcopy(self.elementTree)
      localCrossMembsList = copy.deepcopy(self.listCrossMembers)
      
    
      #(START)determining the motion to be carried out perform it 
      deformotion = 1111111
      for j in i:
        if j.dLength < deformotion:
          deformotion = j.dLength
      deformotion = round(deformotion,1)
      

      ledByNormalMember = True

      deformLeadingNodes = deformationCrossMembers.getDeformLeadNodes(localtree[counter])
      deformotionCrossMembs = deformationCrossMembers.deformAmountCrossMembers(deformLeadingNodes , localCrossMembsList)
      if deformotionCrossMembs < deformotion:
        ledByNormalMember = False  # flag whether the current deformation step is led by the deformable length of cross members or normal members
        deformotion = deformotionCrossMembs

      if deformotion == deformotionCrossMembs:
        logger.info("deformation to be carried out it {}, and it was defined by a cross member".format(deformotion))
      else:
        logger.info("deformation to be carried out it {}, and it was defined by a normal member".format(deformotion))
      #(END)determining the motion to be carried out perform i
      

      #(START)determine whether the current branch is valid to lead the deformation
      decidor = 0
      for j in localtree[counter]:
        if j.deformPossibility == True:
          decidor = decidor +1
          logger.info("decidor has incremented by 1")
      logger.info("decidor value now is {}".format(decidor))
      #(END)determine whether the current branch is valid to lead the deformation
        
      #cross members related parameters to determine the validity of the current deformation step, and if so, how we can proceed
      validToCrossMembers = 0 #an indicator to determine whether this branch of the localtree is valid to be taken. If it equals to the number of cross members, then this branch is valid
      #(START)if amount of deformation is not zero, AND the decidor agreed on deforming, then DEFORM!
      validToCrossMembers = deformingFunction.deforming(deformotion, decidor, localtree, counter, ledByNormalMember, localCrossMembsList, validToCrossMembers)
      #increment the crossMembFailureCounter by one
      if validToCrossMembers != len(localCrossMembsList):
        crossMembFailureCounter += 1
      #(END)the deformation process
          
      if validToCrossMembers == len(localCrossMembsList):  #this makes sure that we will continue if the cross members say so
        logger.debug("cross members have allowed the current branch to continue")
        #(START)add a new member to the list that contains all of the next steps resulting from the input step to this object
        if decidor == len(i):
          logger.debug("proceeding for tree tailoring")
          b = self.treeTailoring(localtree)
          if len(b) != 0:
            logger.debug("a new level of trees is created")
            self.nStepsGroup.append(nextstep(b,self.path,i,localCrossMembsList))  ############CHANGE NONE VALUE WHEN IMPLEMENTING CROSS MEMBERS############
        #(END)end of the process of crearing a new tree of the current branch

        #(START)SHOWING a found OoD
          else:
            logger.debug("treeTailoring function has returned a ZERO sized tree, and the solver has converged to an OoD!")
            print('one OoD is:')
            for x in self.path:
              for y in x:
                print(y.name)
              print('...........')
            for x in i:
              print(x.name)
            print('end of this found OoD!')   
        #(END)SHOWING a found OoD

      if validToCrossMembers != len(localCrossMembsList) and crossMembFailureCounter == len(localtree):
        logger.debug("the solver has converged to an OoD, and the cross members have played a role in aborting")
        print('one OoD is:')
        for x in self.path:
          for y in x:
            print(y.name)
          print('...........')
        print('end of this found OoD!')


      counter = counter +1 #increment the counter by one to go to the next tuple
  



