from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
import copy
from itertools import combinations,groupby

import helpFunctions

# ~p --> not p
# p | q  --> p or q
# p & q --> p and q
# p >> q --> p implies q
# p << q --> q implies p
# Eqivalent(p,q) --> p if and only if q
# (p & q) | (~p & q)

class BeliefBase:
    def __init__(self):
        self.beliefs = []
        self.values = {}
    
    def print(self):
        if len(self.beliefs) == 0:
            print('Knowledge base is empty')
            return
        print('Current beliefs:')
        for belief in self.beliefs:
            print(str(belief) + ', value: ' + str(self.values[str(belief)]))

    def empty(self):
        self.beliefs = []
        self.values = {}

    def add(self, base, belief, value=-1):
        formula = to_cnf(belief)

        base.append(formula)
        if value != -1:
            self.values[str(formula)] = value

    def resolution(self, beliefBase, newBelief):
        tmpBeliefBase = []
        formula = to_cnf(newBelief)
        neg_formula = to_cnf(~formula)

        tmpBeliefBase += helpFunctions.conjuncts(neg_formula)
        for belief in beliefBase:
            tmpBeliefBase += helpFunctions.conjuncts(belief)
        tmpBeliefBase = helpFunctions.removeAllDuplicates(tmpBeliefBase)

        result = set()
        while True:
            # Generate all pairs of clauses
            for pair in combinations(tmpBeliefBase, 2):
                resolvents = helpFunctions.resolve(pair[0], pair[1])
                if False in resolvents:
                    # Arrived to contradiction
                    return True
                # Add resolvent to knowledge base
                result = result.union(set(resolvents))

            if result.issubset(set(tmpBeliefBase)):
                # We are looping
                return False
            else:
                for x in result:
                    if x not in tmpBeliefBase:
                        tmpBeliefBase.append(x)

    def getRemainders(self, belief):
        beliefCnf = to_cnf(belief)
        if not self.resolution(self.beliefs, beliefCnf):
            # Whole knowledge base is solution
            return [self.beliefs]

        solutions = []
        allBeliefs = self.beliefs

        def contract(beliefList, beliefToRemove):
            if len(beliefList) == 1:
                if not self.resolution(beliefList, beliefToRemove):
                    solutions.append(beliefList)
                return
            
            for i in beliefList:
                tmp = helpFunctions.removeFromList(i, beliefList)
                if self.resolution(tmp, beliefToRemove):
                    # Implies beliefToRemove, have to remove more
                    contract(tmp, beliefToRemove)
                else:
                    # Does not imply beliefToRemove, one of the possible solutions
                    solutions.append(tmp)
        
        contract(allBeliefs, beliefCnf)

        # Remove duplicates and solutions that are not maximal (remainders)
        solutions = helpFunctions.removeSublist(solutions)

        return solutions

    def contraction(self, belief, value):
        remainders = self.getRemainders(belief)
        value = float(value)

        maxCertaintyGlobal = 0.0
        if self.values:
            maxCertaintyGlobal = max(self.values.values())

        maxCertainty = -10**10
        maxCertaintyCombined = 0.0
        bestRemainder = []
        # Find the remainder containing the highest certainty value
        # If there are more than one remainder containing the highest certainty value,
        # choose the one with the highest combined certainty
        for r in remainders:
            tmpSum = sum(self.values[str(c)] for c in r)
            for c in r:
                tmpValue = self.values[str(c)]
                if tmpValue > maxCertainty:
                    maxCertainty = tmpValue
                    maxCertaintyCombined = tmpSum
                    bestRemainder = r
                elif tmpValue == maxCertainty:
                    if tmpSum > maxCertaintyCombined:
                        bestRemainder = r


        if maxCertainty < maxCertaintyGlobal and value < maxCertaintyGlobal:
            # By doing the revision we would remove some belief that we are more certain of
            # than the belief that we are trying to add, so we decide not to do it
            return

        self.beliefs = bestRemainder

    def revision(self, belief, value):
        formula = to_cnf(belief)
        negFormula = ~formula
        if self.resolution([], negFormula):
            print('\nInconsistent formulas cannot be added to the knowledge base')
            return
        if formula in self.beliefs:
            # Revising with a formula already in the knowledge base is updating the certainty value for that formula
            self.values[str(formula)] = float(value)
            return
        self.contraction(negFormula, value)
        self.add(self.beliefs, formula, float(value))