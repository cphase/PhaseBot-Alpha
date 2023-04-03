import methods
import pickle
import random

#TODO: difference measure

aiName = "PhaseBot"
userName = input("Enter your name: ")

responseDict = {}
threshold = 0.751

with open("responseDict.pkl","rb") as file:
  responseDict = pickle.load(file)

#PRINT THE DICTIONARY FOR TESTING
printDict = False

if printDict:
  print("DICTIONARY FROM FILE: ")
  print("-------------------------------")
  methods.printDict(responseDict)
  print("-------------------------------")


dictChanged = False

if userName == "fixStrings":
  responseDict = methods.fixStrings(responseDict)
  dictChanged = True;

if userName == "removeResponse":
  responseToRemove = input("What response would you like to remove?: ")
  removedKey = None
  for key in responseDict.keys():
    if responseToRemove in responseDict[key]:
      responseDict[key].remove(responseToRemove)
      removedKey = key
  if len(responseDict[removedKey]) == 0:
        responseDict.pop(removedKey)
  dictChanged = True;

if userName == "reformat":
  responseDict = methods.reformat(responseDict)
  dictChanged = True;

if userName == "trainer":
  lastTrainerInput = ""
  
  print("Begin Training.")
  trainerInput = input("Trainer: ")
  
  while trainerInput != "-1":
    #make formatted versions of input to use as keys
    formatTrainerInput = ' '.join(methods.getWords(trainerInput))
    formatLastTrainerInput = ' '.join(methods.getWords(lastTrainerInput))

    #check if we've seen this message before
    if formatLastTrainerInput in responseDict:
      #check if this response is already in list
      if not trainerInput in responseDict[formatLastTrainerInput]:
        responseDict[formatLastTrainerInput].append(trainerInput)
    else:
      responseList = [trainerInput]
      responseDict[formatLastTrainerInput] = responseList
    lastTrainerInput = trainerInput
    trainerInput = input("Trainer: ")
  dictChanged = True;

if dictChanged and printDict:
  print("DICTIONARY AFTER CHANGES: ")
  print("-------------------------------")
  methods.printDict(responseDict)
  print("-------------------------------")

message = input(aiName + ": " + "Hey, what's up?\n" + userName + ": ")
lastAiMessage = "Hey, what's up?"

while message != "-1":
  #format messages
  formatMessage = ' '.join(methods.getWords(message))
  formatLastAiMessage = ' '.join(methods.getWords(lastAiMessage))
  
  #check if we've seen the message before
  if formatMessage in responseDict:
    #respond with a random message from the response list
    randomIndex = random.randint(0, len(responseDict[formatMessage]) - 1)
    currentResponse = responseDict[formatMessage][randomIndex]
    print(aiName + ": " + currentResponse)
    #save the last interaction
    #check if we've seen the last AI response before as a message
    if formatLastAiMessage in responseDict:
      #check if we already have this response
      if not message in responseDict[formatLastAiMessage]:
        responseDict[formatLastAiMessage].append(message)
    else:
      responseList = [message]
      responseDict[formatLastAiMessage] = responseList
    lastAiMessage = currentResponse

  #if we haven't seen this message before
  else:
    #check if there is a similar enough message to use the responses of
    similarMessages = []
    reverseSimilarity = []
    foundSimilar = False
    for key in responseDict.keys():
      sF = methods.similarity(formatMessage, key)
      sR = methods.similarity(key, formatMessage)
      if (sF >= threshold and sR >= threshold):
        foundSimilar = True
        similarMessages.append(key)
        reverseSimilarity.append(sR)
        
    if foundSimilar:
      #use the closest key if there are multiple that meet the threshold.
      responseIndex = 0;
      for i in range(1, len(similarMessages)):
        if (reverseSimilarity[i] > reverseSimilarity[responseIndex]):
          responseIndex = i
      newKey = similarMessages[responseIndex]
      #now create the response as if we had that key

       #respond with a random message from the response list
      randomIndex = random.randint(0, len(responseDict[newKey]) - 1)
      currentResponse = responseDict[newKey][randomIndex]
      print(aiName + ": " + currentResponse)
      print("\t(USED SIMILAR KEY)")
      
      #save the last interaction
      #check if we've seen the last AI response before as a message
      if formatLastAiMessage in responseDict:
        #check if we already have this response
        if not message in responseDict[formatLastAiMessage]:
          responseDict[formatLastAiMessage].append(message)
      else:
        responseList = [lastAiMessage]
        responseDict[formatLastAiMessage] = message
      lastAiMessage = currentResponse

    else:
      #build the prompt
      cantRespondMessage = aiName
      cantRespondMessage += ": Sorry, idk how to respond to that. Please respond for me!\n"
      cantRespondMessage += aiName + ": "
      
      response = input(cantRespondMessage)
      responseList = [response]
      responseDict[formatMessage] = responseList
      lastAiMessage = response

  #get response
  message = input(userName + ": ")

#get some stats
numKeys = 0
numResponses = 0
for key in responseDict.keys():
  numKeys += 1
  for response in responseDict[key]:
    numResponses += 1

print()
print("***********")
print("{} Keys.".format(numKeys))
print("{} Responses.".format(numResponses))
print("Saving...")

#save the dict
with open("responseDict.pkl","wb") as file:
  pickle.dump(responseDict, file)
  print("Saved!")
  
print("***********")