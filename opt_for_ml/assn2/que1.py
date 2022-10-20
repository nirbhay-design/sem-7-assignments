import numpy as np
import pandas as pd
import cvxopt as cp
import json, sys

json_file = sys.argv[1]
with open(json_file, 'r') as jf:
    data = json.load(jf)

c=np.array(data['c'])
A=np.array(data['A'])
b=np.array(data['b'])
aeq = np.array(data['aeq'])
beq = np.array(data['beq'])

sol = cp.solvers.lp(cp.matrix(
    c,tc="d"), 
    cp.matrix(A,tc="d"),
    cp.matrix(b,tc="d"),
    cp.matrix(aeq,tc='d'), # error in named parameters
    cp.matrix(beq,tc='d'),
    solver=data['solvers'])

print(sol["x"],sol["primal objective"])

"""
Optimal solution found.
[ 6.00e-01]
[ 1.20e+00]
[ 1.02e+01]
 10.199999996490329
"""




