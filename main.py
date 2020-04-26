from knowledgeBase import BeliefBase

beliefBase = BeliefBase()

while True:
    beliefBase.print()
    userInput = input(">>> ")
    beliefBase.add(userInput)