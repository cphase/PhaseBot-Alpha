#Gets the words in a string, all lowercase
def getWords(s):
  onWord = False
  words = []
  tempWord = ""
  for c in s:
    if c.isalpha():
      onWord = True
      tempWord += c.lower()
    elif c == '\'':
      pass
    elif onWord:
      onWord = False
      words.append(tempWord)
      tempWord = ""
  #make sure we add the last word if we end on a letter
  if onWord:
    words.append(tempWord)
  return words
