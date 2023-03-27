import methods
import pickle
import random

aiName = "PhaseBot"
userName = input("Enter your name: ")

responseDict = {}

with open("responseDict.pkl","rb") as file:
  responseDict = pickle.load(file)

if userName == "trainer":
  lastTrainingMessage = ""
  
  print("Begin Training.")
  trainerInput = input("Trainer: ")
  
  while trainerInput != "-1":
    if lastTrainingMessage in responseDict:
      if not trainerInput in responseDict[lastTrainingMessage]:
        responseDict[lastTrainingMessage].append(trainerInput)
    else:
      responseList = [trainerInput]
      responseDict[lastTrainingMessage] = responseList
    lastTrainingMessage = trainerInput
    trainerInput = input("Trainer: ")
    

message = input(aiName + ": " + "Hey, what's up?\n" + userName + ": ")
lastUserMessage = ""
lastAiMessage = "Hey, what's up?"

while message != "-1":
  #respond
  if message in responseDict:
    currentResponse = responseDict[message][random.randint(0, len(responseDict[message]) - 1)]
    print(aiName + ": " + currentResponse)
    if lastAiMessage in responseDict:
      if not message in responseDict[lastAiMessage]:
        responseDict[lastAiMessage].append(message)
    else:
      responseList = [lastAiMessage]
      responseDict[lastAiMessage] = message
    lastAiResponse = currentResponse
    
  else:
    #TODO: figure out how to find a similar message. Maybe get the words, or the keyword and find the closest dictionary key. ignore caps (punctuation already ignored if I use the getwords from journal)
    #start saving keys without punctuation and caps. might have to write a program to process the responseDict that way...
    #will have to process them that way every time we save the key to responseDict or look one up
    #maybe will let us add more responses to other keys if keys are similar enough... but don't want it to start saying anything irrelevant.
    cantRespondMessage = aiName
    cantRespondMessage += ": Sorry, idk how to respond to that. Please respond for me!\n"
    cantRespondMessage += aiName + ": "
    
    response = input(cantRespondMessage)
    responseList = [response]
    responseDict[message] = responseList

  #get response
  
  lastUserMessage = message
  message = input(userName + ": ")

with open("responseDict.pkl","wb") as file:
  pickle.dump(responseDict, file)