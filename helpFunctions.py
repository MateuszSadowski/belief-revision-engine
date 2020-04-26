"""
  
The MIT License (MIT)

Copyright (c) 2016 aima-python contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

def dissociate(op, clause):
    result = []

    def collect(clause):
        args = clause.split(op)
        for arg in args:
            if len(arg.split(op)) > 1:
                collect(arg)
            else:
                result.append(arg)
    collect(clause)
    return result
                
def disjuncts(clause):
    return dissociate('|', clause)

#     def collect2(clause):
#   # def pl_resolve(ci, cj):

    # """Return all clauses that can be obtained by resolving clauses ci and cj.
    # >>> pl_resolve(to_cnf(A|B|C), to_cnf(~B|~C|F))
    # [(A | C | ~C | F), (A | B | ~B | F)]
    # """
    # clauses = []
    # for di in disjuncts(ci):
    #     for dj in disjuncts(cj):
    #         if di == ~dj or ~di == dj:
    #             dnew = unique(removeall(di, disjuncts(ci)) +
    #                           removeall(dj, disjuncts(cj)))
    #             clauses.append(NaryExpr('|', *dnew))
    # return clauses

# def Resolve(c1,c2):
#         #       resolvents = Resolve(Ci,Cj)
#     clauses = []
#     for d_c1 in disjuncts(c1):
#         for d_c2 in disjuncts(c2):
#             if d_c1 == ~d_c2 or ~d_c1 == d_c2:
#                 new_disjunct = unique((removeall(d_c1, disjuncts(c1)) + removeall(d_c2, disjuncts(c2))))
                
#     return clauses