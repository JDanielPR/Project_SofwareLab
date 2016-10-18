import itertools

def possibilitiesTree_generator( listLoadpaths, listCrossComponents ):

  # Add all of the loadpaths to a list called "structure array" for the sake
  # of the possibilities tree generation using the embedded module itertools
  structureArray = []
  for loadpath in self.listLoadpaths:
    structureArray.append(loadpath.listComponents)

  # Generate the possibilities tree
  possibilitiesTree = list(itertools.product(*structureArray))

  return possibilitiesTree

  
