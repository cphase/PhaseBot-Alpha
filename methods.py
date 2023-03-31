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
  #print(valueList)
  #print(dict)
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
  
  