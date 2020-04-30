from sympy.logic.boolalg import Or, And

def dissociate(op, args):
    result = []

    def collect(subargs):
        for arg in subargs:
            if isinstance(arg, op):
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result

def associate(op, args):
    args = dissociate(op, args)
    if len(args) == 0:
        return op.identity
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)
                
def disjuncts(clause):
    return dissociate(Or, [clause])

def conjuncts(clause):
    return dissociate(And, [clause])

def removeFromList(value, subset):
    return [x for x in subset if x != value]

def removeAllDuplicates(oldList):
    cleanList = []
    for x in oldList:
        if x not in cleanList:
            cleanList.append(x)
    return cleanList

def uniqueValues(subset):
    return list(set(subset))

def removeSublist(lst): 
    curr_res = [] 
    result = [] 
    for ele in sorted(map(set, lst), key = len, reverse = True): 
        if not any(ele <= req for req in curr_res): 
            curr_res.append(ele) 
            result.append(list(ele))
    return result

def resolve(c1,c2):
    clauses = []
    resolvedSomething = False
    for d_c1 in disjuncts(c1):
        for d_c2 in disjuncts(c2):
            if (d_c1 == ~d_c2) or (~d_c1 == d_c2):
                new_disjunct = uniqueValues(removeFromList(d_c1, disjuncts(c1)) + removeFromList(d_c2, disjuncts(c2)))
                clauses.append(associate(Or, new_disjunct)) 
                resolvedSomething = True

    if not resolvedSomething:
        new_disjunct = uniqueValues(disjuncts(c1) + disjuncts(c2))
        clauses.append(associate(Or, new_disjunct)) 

    return clauses


# c1 = (~p AND q)
# c2 = ~(p OR ~q)

# p&q --> p AND q
# (p&q | s) --> (p OR s) AND (q OR s)