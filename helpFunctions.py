"""
  
The MIT License (MIT)

Copyright (c) 2016 aima-python contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

def dissociate(op, clause):
    clause = str(clause)
    result = []

    def collect(clause):
        args = clause.split(op)
        for arg in args:
            if len(arg.split(op)) > 1:
                collect(arg)
            else:
                arg = arg.replace(' ', '')
                result.append(arg)
    collect(clause)
    return result
                
def disjuncts(clause):
    return dissociate('|', clause)

def conjuncts(clause):
    return dissociate('&', clause)

def removeFromList(value, subset):
    return [x for x in subset if x != value]

def removeAllDuplicates(x):
  return list(dict.fromkeys(x))

def uniqueValues(subset):
    return list(set(subset))

def associate(op, clauses):
    if len(clauses) == 0:
        return False
    elif len(clauses) == 1:
        return clauses[0]
    else:
        result = ""
        for i in range(len(clauses)-1):
            result += clauses[i] + "|"
        result += clauses[len(clauses)-1]
    return result

def resolve(c1,c2):
    clauses = []
    resolvedSomething = False
    for d_c1 in disjuncts(c1):
        for d_c2 in disjuncts(c2):
            if (d_c1 == '~' + d_c2) or ('~' + d_c1 == d_c2):
                new_disjunct = uniqueValues(removeFromList(d_c1, disjuncts(c1)) + removeFromList(d_c2, disjuncts(c2)))
                clauses.append(associate('|', new_disjunct)) 
                resolvedSomething = True

    if not resolvedSomething:
        new_disjunct = uniqueValues(disjuncts(c1) + disjuncts(c2))
        clauses.append(associate('|', new_disjunct)) 

    return clauses


# c1 = (~p AND q)
# c2 = ~(p OR ~q)

# p&q --> p AND q
# (p&q | s) --> (p OR s) AND (q OR s)