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
        print('Current beliefs:')
        for belief in self.beliefs:
            print(str(belief) + ', value: ' + str(self.values[str(belief)]))
        print('')

    def add(self, base, belief, value=-1):
        # TODO: validate input (using resolution(?))
        # TODO: handle the case when value not passed
        formula = to_cnf(belief)
        negFormula = ~formula
        if not self.resolution(base, negFormula):
            formula = to_cnf(belief)
            base.append(formula)
            if value != -1:
                self.values[str(formula)] = value

    def resolution(self, beliefBase, newBelief):
        tmpBeliefBase = []
        formula = to_cnf(newBelief)
        neg_formula = to_cnf(~formula)
        # negate the formula
        # formula = (q | ~p)
        # ~formula = (~q & p) by De Morgans law
        # q | ~p --> ~q | ~p
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
                # Add resolvent to belief base
                result = result.union(set(resolvents))

            if result.issubset(set(tmpBeliefBase)):
                # We are looping
                return False
            else:
                for x in result:
                    if x not in tmpBeliefBase:
                        tmpBeliefBase.append(x)
                # tmpBeliefBase += list(result)
                # tmpBeliefBase = helpFunctions.remove_dublicates(tmpBeliefBase)

    def getRemainders(self, belief):
        beliefCnf = to_cnf(belief)
        if not self.resolution(self.beliefs, beliefCnf):
            # Whole belief base is solution
            return [self.beliefs]

        solutions = []
        allBeliefs = []
        for belief in self.beliefs:
            allBeliefs += helpFunctions.conjuncts(belief)
        allBeliefs = helpFunctions.removeAllDuplicates(allBeliefs)
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

    def contraction(self, belief):
        remainders = self.getRemainders(belief)

        print(remainders)

        maxValue = -10**10
        remainderSum = -10**10
        bestSolution = None
        for r in remainders:
            tmpSum = sum(self.values[str(c)] for c in r)
            for c in r:
                tmpValue = self.values[str(c)]
                if tmpValue > maxValue:
                    maxValue = tmpValue
                    remainderSum = tmpSum
                    bestSolution = r
                elif tmpValue == maxValue:
                    if tmpSum > remainderSum:
                        bestSolution = r

        self.beliefs = bestSolution

    def revision(self, belief, value):
        # TODO: Fix case when adding the same formula or then allow to update values
        formula = to_cnf(belief)
        negFormula = ~formula
        self.contraction(negFormula)
        self.add(self.beliefs, belief, value)
        # self.values[str(formula)] = value