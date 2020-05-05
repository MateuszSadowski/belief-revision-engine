from knowledgeBase import BeliefBase
import helpFunctions
from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
import time

beliefBase = BeliefBase()

def printHelpMessage():
    print('========================== MENU ===========================')
    print('Print belief base - put \'p\'')
    print('Print allowed operators for formula input - put \'o\'')
    print('Check if belief base entails formula - put \'c\'')
    print('Revise belief base - put \'r\'')
    print('Empty belief base - put \'e\'')
    print('Quit - put \'q\'')
    print('===========================================================')

def printAllowedOperators():
    print('Allowed operators:')
    print('OR: |')
    print('AND: &')
    print('NEGATION: ~')
    print('IMPLICATION: >>')

def checkEntailment():
    print('Input formula to check:')
    formula = input('>>> ')
    print('')
    try:
        print('Is formula entailed in the belief base: ' + str(beliefBase.resolution(beliefBase.beliefs, formula)))
    except:
        print('Something went wrong, make sure the formula is correct and try again')

def validateValue(value):
    try:
        value = float(value)
    except:
        print('\nPlease input a number in the range of 0.0 to 1.0\n')
        return False
    if value < 0.0 or value > 1.0:
        print('\nPlease input certainty in the range of 0.0 to 1.0\n')
        return False
    return True

def revise():
    print('Input correct propositional logic formula:')
    formula = input('>>> ')
    print('Input certainty of the belief (from 0.0 to 1.0):')
    value = input('>>> ')
    while not validateValue(value):
        print('Input certainty of the belief (from 0.0 to 1.0):')
        value = input('>>> ')
    try:
        beliefBase.revision(formula, value)
    except:
        print('\nSomething went wrong, make sure the formula is correct and try again')

def mainLoop():
    while True:
        printHelpMessage()
        print('Choose action:')
        action = input('>>> ')
        print('')
        if action == 'p':
            beliefBase.print()
        elif action == 'o':
            printAllowedOperators()
        elif action == 'c':
            checkEntailment()
        elif action == 'r':
            revise()
            print('')
            beliefBase.print()
        elif action == 'e':
            beliefBase.empty()
            beliefBase.print()
        elif action == 'q':
            break
        else:
            print('Unrecognized action')      
        print('')
        time.sleep(1)

mainLoop()
