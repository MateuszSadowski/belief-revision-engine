from knowledgeBase import BeliefBase
import helpFunctions
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
import utils

beliefBase = BeliefBase()

# while True:
    # beliefBase.print()
    # userInput = input(">>> ")
beliefBase.add('p|q')
beliefBase.add('~q&r')
# beliefBase.add('p<<q')

beliefBase.print()

print(beliefBase.resolution('p>>q'))