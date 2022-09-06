import numpy as np
import pandas as pd
import cvxopt as cp
import json, sys

json_file = sys.argv[1]
with open(json_file, 'r') as jf:
    data = json.load(jf)

c=np.array(data['c'])
A=np.eye(*data['A'])
b=np.array(data['b'])
aeq = np.array(data['aeq'])
beq = np.array(data['beq'])

sol = cp.solvers.lp(
    cp.matrix(c,tc="d"), 
    cp.matrix(A,tc="d"),
    cp.matrix(b,tc="d"),
    cp.matrix(aeq,tc='d'),
    cp.matrix(beq,tc='d'),
    solver = data["solvers"])

print(sol["x"],sol["primal objective"])

"""
OPTIMAL LP SOLUTION FOUND
[ 1.00e+00]
[ 1.00e+00]
[ 2.00e+00]
[ 1.00e+00]
[ 1.00e+00]
 14.0
"""