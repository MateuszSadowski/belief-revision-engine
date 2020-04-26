from sympy.logic.boolalg import to_cnf, And, Or, Equivalent

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
        newBelief = {}
        if fromConsole:
            newBelief["input"] = belief
        else:
            newBelief["input"] = formula
        newBelief["formula"] = formula

        self.beliefs.append(newBelief)