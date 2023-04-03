#Gets the words in a string, all lowercase
def getWords(s):
  onWord = False
  words = []
  tempWord = ""
  for c in s:
    if c.isalnum():
      onWord = True
      tempWord += c.lower()
    elif c == '\'' or c == ':':
      pass
    elif onWord:
      onWord = False
      words.append(tempWord)
      tempWord = ""
  #make sure we add the last word if we end on a letter
  if onWord:
    words.append(tempWord)
  return words

#reformats the dictionary to only use words/numbers and lowercase
def reformat(dict):
  newDict = {}
  valueList = list(dict.values())
  #a list of lists of responses
  keyList = list(dict.keys())
  #print(keyList)
  keyDict = {}
  #make a dictionary that will get the previous key
  for key in keyList:
    keyDict[key] = ' '.join(getWords(key))
  #print(keyDict)

  for i in range(0, len(keyList)):
    newDict[keyDict[keyList[i]]] = valueList[i]

  return newDict

#checks what % of words in s1 are in s2
def similarity(s1, s2):
  if s1 == "":
    return 0
  l1 = getWords(s1)
  l2 = getWords(s2)
  same = 0
  for word in l1:
    if word in l2:
      same += 1

  return same / len(l1)

#fixes if the value is a string instead of a list of strings
def fixStrings(dict):
  newDict = {}
  for key in dict.keys():
    if type(dict[key]) is str:
      tempList = [dict[key]]
      newDict[key] = tempList
    elif isinstance(dict[key], list):
      newDict[key] = dict[key]

  return newDict

#prints the dictionary in a more readable format
def printDict(dict):
  for key in dict.keys():
    print(key)
    print(dict[key])
    print()