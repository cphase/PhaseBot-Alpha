import methods
import pickle
import random

aiName = "PhaseBot"
userName = input("Enter your name: ")

responseDict = {}

with open("responseDict.pkl","rb") as file:
  responseDict = pickle.load(file)

if userName == "reformat":
  #IF WE WANT TO ACTUALLY REFORMAT, THEN SET DICT EQUAL TO THIS
  #dont do that until we have it setup to add to it properly in all cases
  methods.reformat(responseDict)

if userName == "trainer":
  lastTrainerInput = ""
  
  print("Begin Training.")
  trainerInput = input("Trainer: ")
  
  while trainerInput != "-1":
    #make formatted versions of input to use as keys
    formatTrainerInput = methods.getWords(trainerInput)
    formatLastTrainerInput = methods.getWords(lastTrainerInput)

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
  formatMessage = methods.getWords(message)
  formatLastUserMessage = methods.getWords(lastUserMessage)
  formatLastAiMessage = methods.getWords(lastAiMessage)
  
  #check if we've seen the message before
  if formatMessage in responseDict:
    #respond with a random message from the response list
    currentResponse = responseDict[formatMessage][random.randint(0, len(responseDict[message]) - 1)]
    print(aiName + ": " + currentResponse)
    #check if we've seen the last AI response before as a message
    if formatLastAiMessage in responseDict:
      #check if we already have this response
      if not message in responseDict[lastAiMessage]:
        responseDict[formatLastAiMessage].append(message)
    else:
      responseList = [lastAiMessage]
      responseDict[formatLastAiMessage] = message
    lastAiResponse = currentResponse
    
  else:
    #TODO: figure out how to find a similar message. Maybe get the words, or the keyword and find the closest dictionary key. ignore caps (punctuation already ignored if I use the getwords from journal).
    #maybe will let us add more responses to other keys if keys are similar enough... but don't want it to start saying anything irrelevant.
    
    #build our prompt
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