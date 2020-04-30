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
    
    def print(self):
        print('Current beliefs:')
        for belief in self.beliefs:
            print(str(belief))

    def add(self, base, belief):
        # TODO: validate input
        formula = to_cnf(belief)
        base.append(formula)

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

    def contraction(self, belief):
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

    # solutions = [for s1]        

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


    # ==== CONTRACTION ALGORITHM ===
    # 1. Enumerate all
    # (p | q) & (~p | z) & p & ~q
    # remove (p|q)
    # result: (~p | z) & p & ~q
    # remove (~p | z)
    # result: (p | q) & p & ~q
    

    # "K remainder q" (reversed(T))
    # for every combination
    #       apply resolution of q (~q) on combination
    #       if q not implies
    #           add to options
    #       else
    #           discard
    # for options
    #       test for maximum (how?) (maximum in terms of adding behavior)
    #       try to add every combination of what is in the belief base but not in the option
    #       and see if it then implies queue
    #       if it does imply q for anything you can add then it is then maximal
    # a, b, c 
    # a,b     a,c     b,c     a      b      c      a,b,c