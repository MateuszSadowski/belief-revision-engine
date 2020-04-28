from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
import copy
from itertools import combinations

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
        # belief.input -> what user inputed in natural form
        # belief.formula -> belief in CNF form
        self.beliefs = []
        #[
        # {
        # "input": "p >> q",
        # "formula": "~p | q"
        # },
        # {
        # "input": "p | q",
        # "formula": "p | q"
        # }
        # ]
    
    def print(self):
        print('Current beliefs:')
        for belief in self.beliefs:
            print(belief["input"])
            # if belief.input:
            #     print(belief.input)
            # else:
            #     print(belief.formula)

    def add(self, belief, fromConsole=True):
        # TODO: validate input
        formula = to_cnf(belief)
        formula = str(formula)
        newBelief = {}
        if fromConsole:
            newBelief["input"] = belief
        else:
            newBelief["input"] = formula
        newBelief["formula"] = formula

        self.beliefs.append(newBelief)

    def resolution(self, newBelief):
        # beliefBase = copy.deepcopy(self.beliefs)
        tmpBeliefBase = []
        formula = to_cnf(newBelief)
        neg_formula = to_cnf(~formula)
        # negate the formula
        # formula = (q | ~p)
        # ~formula = (~q & p) by De Morgans law
        # q | ~p --> ~q | ~p
        tmpBeliefBase += helpFunctions.conjuncts(str(neg_formula))
        for belief in self.beliefs:
            tmpBeliefBase += helpFunctions.conjuncts(belief['formula'])
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
                


    # KB is knowledge base # q is new sentence of logic
    # clauses = contra(KB,q) -------> KB & ~a
    # new = {}
    # while True:
    #   for each pair of clauses Ci,Cj in clauses
    #       resolvents = Resolve(Ci,Cj)
    #       if resolvents contains the empty clause
    #           return true
    #       new += resolvents
    #       if new is subset of clauses
    #           return false
    #       clauses += new