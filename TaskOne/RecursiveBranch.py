import logging
import Deform
import OtherFunctions
from isdh import deformation_step

logger = logging.getLogger('RecursiveBranch')
logging.basicConfig(level=logging.DEBUG)

class RecursiveBranch():

  #initialization of the created object
  def __init__(self,
               possibilitiesTree,
               history,
               previousStep,
               listCrossComponents,
               listLoadpaths,
               counter,
               solutionFile):

    logger.debug("stepped into another level")

    self.possibilitiesTree = possibilitiesTree
                                                                    
    # List of all possibilities trees resulting from the motion undertaken by
    # each branch of the input possibilites tree
    self.resultingPossiblitiesTrees = []

    #stores the previously performed steps that led to the current tree of
    #possibilities
    self.solutionPath = []
    if history is None:
      pass
    else:
      for element in history:
        self.solutionPath.append(element)

    #append the step resulted this tree of possibilities into "path"
    if previousStep is not None:
      self.solutionPath.append(previousStep)
    else:
      pass
    
    '''
    self.solutionPath = history
    for member in previousStep:
      self.solutionPath[].append(member)
    '''
    
    self.listCrossComponents = listCrossComponents
    self.listLoadpaths = listLoadpaths
    self.solutionCounter = counter
    self.solutionFile = solutionFile
    #self.OoDSolutions = OoDSolutions
    self.carry_on()  

  def carry_on(self):
    '''Function

    Function 
    '''
    #counter = 0
    #print("statrt with ",counter/len(self.possibilitiesTree)*100,"% of current level")

    # Counter for the number times that the possibilitiesTree's branch
    # has been skipped due to the violation of the assumptions related
    # to cross components
    crossComponentsFailureCounter = 0
    
    # Counter for the number of times the deformation did not take
    # place due to the presence of OFF members in the selected tuple
    numberRigidComponentTerminations = 0
    solutionBranch = 0
    #availableTuplesToDeform gives us an idea of the number of possibilitiesTree
    #branches that are capable of deforming
    availableTuplesToDeform = len(self.possibilitiesTree)
    for branch in self.possibilitiesTree:
      for component in branch:
        if component.calc_length() == component.rigidLength:
          availableTuplesToDeform -= 1
          break
        else:
          pass
    ledByComponent = True

    #loop over all the branches of the possibilitiesTree
    for branch in self.possibilitiesTree:

      decidor = 0
      #Determine if this branch has any components not able to deform
      for component in branch:
        if component.perminantlyBlockedDeformation is False:
          numberRigidComponentTerminations +=1
          break
        else:
          pass
        if component.temporarilyBlockedDeformation is True:
          decidor += 1
        else:
          pass

      validToCrossComponents = False


      if decidor == len(branch):
        solutionBranch = branch

        #Calculation of the motion to be carried out from the deformable length
        #of components
        deformationAmount = 10000.00000 #some big value
        for component in branch:
          if (component.calc_length() - component.rigidLength) < deformationAmount:
            deformationAmount = component.calc_length() - component.rigidLength
          else:
            pass
        deformationAmount = round(deformationAmount,1)
        print("deformationAmount is: ",deformationAmount)
        
        #ledByComponent is a flag that indicates whether a deformation step is
        #detemined by the length of components or cross-components

        
        #Get the nodes that are leading the deformation
        deformationLeadingNodes = OtherFunctions.get_deformation_nodes(branch)
        
        #Calculate the deformation that is allowed by the whole deforming
        #cross-components
        deformationAmountCrossComponents = (
          OtherFunctions.deformation_amount_cross_components(
            deformationLeadingNodes,
            self.listCrossComponents
          )
        )
        
        #Compare between the defomation step allowed by the normal components with the
        #one allowed by cross-components and change the corresponding flag accordingly
        if deformationAmountCrossComponents < deformationAmount:
          ledByComponent = False  
          deformationAmount = deformationAmountCrossComponents
        else:
          pass

        if deformationAmount == deformationAmountCrossComponents:
          logger.info("deformation to be carried out it {}, and it was defined by a cross member".format(deformationAmount))
        else:
          logger.info("deformation to be carried out it {}, and it was defined by a normal member".format(deformationAmount))

        #validToCrossComponents decides the agreement of the deformation
        #step taken with the cross components. If this deformation is valid to
        #cross components, then validToCrossComponents is True, if not, then
        #it is False
        #validToCrossComponents = False
        #peform the deformation step upon the components
        validToCrossComponents = Deform.deform(
          deformationAmount,
          decidor,
          branch,
          ledByComponent,
          self.listCrossComponents,
          validToCrossComponents,
          self.listLoadpaths
        )
        print("validToCrossMembers value is",validToCrossComponents)

        #increment the crossComponentFailureCounter by one is this deformation step
        #was not valid to cross-components
        if validToCrossComponents is False:
          crossComponentsFailureCounter += 1
        else:
          pass


        #Now, we will continue if the cross-components allows to do so
        if validToCrossComponents is True and deformationAmount != 0:
          logger.debug("cross members have allowed the current branch to continue")

          noLoadpathsWithOneDeformComponent = 0
          '''
          for loadpath in self.listLoadpaths:
            if len(loadpath.listComponents) - loadpath.noComponentsNotDeformable >= 1:
              noLoadpathsWithOneDeformComponent += 1
            else:
              pass
          for loadpath in self.listLoadpaths:
            for comp in loadpath.listComponents:
              print(comp.perminantlyBlockedDeformation)
          '''
          
          #if noLoadpathsWithOneDeformComponent == len(self.listLoadpaths):
          logger.debug("a new level of possiblities trees has been created")
          self.resultingPossiblitiesTrees.append (
            RecursiveBranch (
              self.possibilitiesTree,
              self.solutionPath,
              branch,
              self.listCrossComponents,
              self.listLoadpaths,
              self.solutionCounter,
              self.solutionFile
            )
          )
          #else:
          #  pass

        else:
          pass
        if deformationAmount != 0:
          # retrieve the members and the cross members to their state before this already performed deformation step
          OtherFunctions.restore(branch, self.listLoadpaths, self.listCrossComponents)
        else:
          pass
      else:
        pass
      #counter += 1
      #print("finished now with ",round(counter/len(self.possibilitiesTree),2)*100,"% of current level")

    #Solution is output when all of the branches have been forbidden from going on
    #because their deformations have violated the cross-components' assumptions
    '''
    if availableTuplesToDeform == crossComponentsFailureCounter:
      #print_solution()
      print("SOLUTION FOUND")
      logger.debug("the solver has converged to an OoD, and the cross members have played a role in aborting")
      print("numberOffMemberTerminations is:", numberRigidComponentTerminations)
      print('one OoD is:')
      for x in self.solutionPath:
        for y in x:
          print(y.name)
        print('...........')
      print('end of this found OoD!')
      self.solutionCounter.increase()
    else:
      pass
    '''
    #if len(self.listCrossComponents) == 0 and availableTuplesToDeform == 1 and crossComponentsFailureCounter == 0:
    if availableTuplesToDeform == 0 or availableTuplesToDeform == crossComponentsFailureCounter:
      #print('one OoD is:')
      #for x in self.solutionPath:
      #  for y in x:
      #    print(y.name)
      #  print('...........')
      self.solutionFile.write('__________________________________')
      self.solutionFile.write("\n")
      self.solutionFile.write('one OoD is:')
      self.solutionFile.write("\n")
      for x in self.solutionPath:
        for y in x:
          self.solutionFile.write(y.name)
          self.solutionFile.write("\n")
        self.solutionFile.write('.........')
        self.solutionFile.write("\n")
      #for member in solutionBranch:
      #  print(member.name)
      self.solutionFile.write('end of this found OoD!')
      self.solutionFile.write("\n")
      self.solutionFile.write('__________________________________')
      self.solutionFile.write("\n")
      self.solutionCounter.increase()
    else:
      pass
