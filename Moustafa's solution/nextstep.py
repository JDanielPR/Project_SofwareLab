import member
import loadpath
import logging
import gapsHandeling
import deformationCrossMembers 
import deformingFunction
import otherFunctions as others

logger = logging.getLogger('nextstep')
logging.basicConfig(level=logging.DEBUG)

class nextstep():

  #initialization of the created object
  def __init__(self, possibilitiesTree, history, previousStep, listCrossMembers, listLoadpaths,counter):

    #input tree for this object to start from
    self.elementTree = possibilitiesTree

    logger.debug("steped into another level has {} possibilities".format(len(self.elementTree)))
                                                                    
    #list of all possibilities trees resulting from the motion undertaken by each tuple of the input tree for this object
    self.resultingPossiblitiesTree = []

    #stores the previously performed steps that led to the current tree of possibilities
    if history is None:
      self.solutionPath = []
    else:
      self.solutionPath = history

    #append the step resulted this tree of possibilities into "path"
    if previousStep is not None:
      self.solutionPath.append(previousStep)

    self.listCrossMembers = listCrossMembers
    self.listLoadpaths = listLoadpaths
    self.solutionCounter = counter

    self.carryon()  

  #resposible function for performing the procedure of stepping
  def carryon(self):

    counter = 0

    #counter for the times that the tree's branch has been skipped due to the violation of the assumptions related to cross members
    crossMembFailureCounter = 0
    #counter that counts the number of times the deformation did not take place due to the presence of OFF members in the selected tuple
    numberOffMemberTerminations = 0

    availableTuplesToDeform = len(self.elementTree)
    for i in self.elementTree:
        for m in i:
            if m.state == False:
                availableTuplesToDeform -= 1
                break

    #loop over all the branches of the passed OoD tree 
    for i in self.elementTree:
      
      #Determine if this tuple has any OFF members
      anyOffMembers = False
      for member in self.elementTree[counter]:
        print("member state is:", member.state)
        if member.state is False:
          anyOffMembers = True
          numberOffMemberTerminations +=1
          print("numberOffMemberTerminations value is :",numberOffMemberTerminations)
          break

      validToCrossMembers = False

      if anyOffMembers is False:
        print("hello")
        #(START)determining the motion to be carried out 
        #Calculation of the motion to be carried out from the deformable length of normal members (not cross)
        deformotion = 1111111
        for j in self.elementTree[counter]:
          if j.dLength < deformotion:
            deformotion = j.dLength
        deformotion = round(deformotion,1)
        #Turn this flag on, which indicates that the motion is carried out by normal members (for now!)
        ledByNormalMember = True
        #Get the nodes that are leading the deformation
        deformLeadingNodes = deformationCrossMembers.getDeformLeadNodes(self.elementTree[counter])
        #Calculate the deformation that is allowed by the whole deforming cross members
        deformotionCrossMembs = deformationCrossMembers.deformAmountCrossMembers(deformLeadingNodes , self.listCrossMembers)
        #Compare between the defomation step allowed by the normal members with the one allowed by cross members and change the corresponding flag accordingly
        if deformotionCrossMembs < deformotion:
          ledByNormalMember = False  # flag whether the current deformation step is led by the deformable length of cross members or normal members
          deformotion = deformotionCrossMembs
        #Loggers to classify the what kind of members that determined this deformation amount
        if deformotion == deformotionCrossMembs:
          logger.info("deformation to be carried out it {}, and it was defined by a cross member".format(deformotion))
        else:
          logger.info("deformation to be carried out it {}, and it was defined by a normal member".format(deformotion))
        #(END)determining the motion to be carried out

        #(START)determine whether the current tuple of normal members are allowed to deform
        decidor = 0
        for j in self.elementTree[counter]:
          print("member", j.name, "has state", j.state)
          if j.deformPossibility == True and j.state == True:
            decidor = decidor +1
            logger.info("decidor has incremented by 1")
        logger.info("decidor value now is {}".format(decidor))
        #(END)determine whether the current tuple of normal members are allowed to deform
        
        #cross members related parameters to determine the validity of the current deformation step, and if so, how we can proceed
        validToCrossMembers = False #an indicator to determine whether this branch of the localtree is valid to be taken. If it equals to the number of cross members, then this branch is valid
        #(START)if amount of deformation is not zero, AND the decidor agreed on deforming, then DEFORM!
        validToCrossMembers = deformingFunction.deform(deformotion, decidor, self.elementTree, counter, ledByNormalMember, self.listCrossMembers, validToCrossMembers, self.listLoadpaths)
        print("validToCrossMembers value is",validToCrossMembers)
        #increment the crossMembFailureCounter by one
        if validToCrossMembers is False:
          crossMembFailureCounter += 1 #this is used to abort a solution at the end of the for loop because all the current possibilities violate cross members' assumptions
        #(END)the deformation process
          
        if validToCrossMembers is True:  #this makes sure that we will continue if the cross members say so
          logger.debug("cross members have allowed the current branch to continue")
          #(START)add a new member to the list that contains all of the next steps resulting from the input step to this object
          if decidor == len(i): 
            x = 0 #this variable "x" counts the number of loadpaths that have at least 1 member ready to get deformed
            for loadpath in self.listLoadpaths.listOfLoadpaths:
              if len(loadpath.listOfMembers) - loadpath.noOffMembers >= 1:
                x += 1
            if x == len(self.listLoadpaths.listOfLoadpaths):
              logger.debug("a new level of trees is created")
              self.resultingPossiblitiesTree.append(nextstep(self.elementTree,self.solutionPath,i,self.listCrossMembers,self.listLoadpaths,self.solutionCounter))
              self.solutionPath.remove(self.solutionPath[len(self.solutionPath)-1])



            print("Return to the previous level of trees")


          #(END)end of the process of creating a new tree of the current branch

        if availableTuplesToDeform == 1 and validToCrossMembers is True:
           logger.debug("Non of the possibilities has members able to deform again, so the solver has converged to an OoD!")
           print('one OoD is:')
           for x in self.solutionPath:
               for y in x:
                  print(y.name)
               print('...........')
           for memb in self.elementTree[counter]:
               print(memb.name)
           print('end of this found OoD!')
           self.solutionCounter.increase()


        #retrieve the members and the cross members to their state before this already performed deformation step
        if decidor == len(self.elementTree[counter]) and deformotion != 0 :
           others.restore(self.elementTree, counter, self.listLoadpaths, self.listCrossMembers)

      print("the counter is:" ,counter)
      # increment the counter by one to go to the next tuple
      counter = counter + 1

      if crossMembFailureCounter == (len(self.elementTree) - numberOffMemberTerminations):  # The second conditions states that if this whole level is not valid to crossMembers, then it will return the length of the possibilities tree
          logger.debug("the solver has converged to an OoD, and the cross members have played a role in aborting")
          print("numberOffMemberTerminations is:", numberOffMemberTerminations)
          print('one OoD is:')
          for x in self.solutionPath:
              for y in x:
                  print(y.name)
              print('...........')
          print('end of this found OoD!')
          self.solutionCounter.increase()
