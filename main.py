import methods
import pickle
import random

#TODO: difference measure
#      remove function

aiName = "PhaseBot"
userName = input("Enter your name: ")

responseDict = {}

with open("responseDict.pkl","rb") as file:
  responseDict = pickle.load(file)

if userName == "removeResponse":
  responseToRemove = input("What response would you like to remove?: ")
  removedKey = None
  for key in responseDict.keys():
    if responseToRemove in responseDict[key]:
      responseDict[key].remove(responseToRemove)
      removedKey = key
  if len(responseDict[removedKey]) == 0:
        responseDict.pop(removedKey)

if userName == "reformat":
  responseDict = methods.reformat(responseDict)

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

message = input(aiName + ": " + "Hey, what's up?\n" + userName + ": ")
lastUserMessage = ""
lastAiMessage = "Hey, what's up?"

while message != "-1":
  #format messages
  formatMessage = ' '.join(methods.getWords(message))
  formatLastUserMessage = ' '.join(methods.getWords(lastUserMessage))
  formatLastAiMessage = ' '.join(methods.getWords(lastAiMessage))
  
  #check if we've seen the message before
  if formatMessage in responseDict:
    #respond with a random message from the response list
    randomIndex = random.randint(0, len(responseDict[formatMessage]) - 1)
    currentResponse = responseDict[formatMessage][randomIndex]
    print(aiName + ": " + currentResponse)
    #check if we've seen the last AI response before as a message
    if formatLastAiMessage in responseDict:
      #check if we already have this response
      if not message in responseDict[formatLastAiMessage]:
        responseDict[formatLastAiMessage].append(message)
    else:
      responseList = [lastAiMessage]
      responseDict[formatLastAiMessage] = message
    lastAiResponse = currentResponse

  #if we haven't seen this message before
  else:
    #build our prompt
    for key in responseDict.keys():
      #TODO: make a list of keys above a certain threshold.
      #then compare them in the other order and use the highest one for a repsonse
      print(key)
      print(methods.similarity(message, key))
    cantRespondMessage = aiName
    cantRespondMessage += ": Sorry, idk how to respond to that. Please respond for me!\n"
    cantRespondMessage += aiName + ": "
    
    response = input(cantRespondMessage)
    responseList = [response]
    responseDict[formatMessage] = responseList

  #get response
  lastUserMessage = message
  message = input(userName + ": ")

with open("responseDict.pkl","wb") as file:
  pickle.dump(responseDict, file)