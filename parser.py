import string
from elements import *


def parse(s): #Single letter only, e.g. 5x allowed but not 4cat
  letters = string.lowercase + string.uppercase
  digits = string.digits
  keys = ["*", "+", "/", "-","(",")","[","]"]

  ############

  noSpaces = s.replace(" ","")
  length = len(noSpaces)

  lastInd = 0 #Last measured index of a key
  splitStrings = []
  
  for ind in range(length):
    if noSpaces[ind] in keys:
      splitStrings += [noSpaces[lastInd:ind], noSpaces[ind:ind+1]]
      lastInd = ind + 1

  splitStrings += [noSpaces[lastInd:]]
  splitStrings = [e for e in splitStrings if e != ""]

  finalList = []
      
  lenSplitStrings = len(splitStrings)
  for splitWord in splitStrings:
    if splitWord[-1] in letters and splitWord[:-1] in digits: #e.g. 22x
      finalList.append(Product(Number(float(splitWord[:-1])), Variable(splitWord[-1])))
    elif splitWord in keys:
      finalList.append(splitWord)
    elif splitWord in letters:
      finalList.append(Variable(splitWord))
    else:
      finalList.append(Number(float(splitWord)))

  return fixify(finalList)
  
def fixify(wordList):
  #Do parens
  #then mults
  #then adds
  l = len(wordList)

  #Finds parens for paren evaluations:
  parenInds = (0,0)
  for wordInd in range(l):
    if wordList[wordInd] == "(" or wordList[wordInd] == "[":
      for wordRevInd in range(l - 1, 0, -1):
        if wordList[wordRevInd] == ")" or wordList[wordRevInd] == ")":
          parenInds = (wordInd, l - 1 - wordRevInd)
    else: #No parens left
      pass #?

  parensEvald = fixify(wordList[parenInds[0]:parenInds[1]]) #Not sure what to do with this yet

  #Find a binary mult, left to right:
  for wordInd in range(l):
    if wordInd == "*":
      multEvald = fixify(wordList[wordInd - 1:wordInd + 2])

  #Miles you can figure out the rest
        
  
print parse("(3x + 53)*24")

