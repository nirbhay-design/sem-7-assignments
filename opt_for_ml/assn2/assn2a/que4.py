import numpy as np
import pandas as pd
import cvxopt as cp
import json, sys

json_file = sys.argv[1]
with open(json_file, 'r') as jf:
    data = json.load(jf)

Q=np.array(data['Q'])
c=np.array(data['c'])
A=np.array(data['A'])
b = np.array(data['b'])

sol = cp.solvers.qp(
    cp.matrix(Q,tc="d"), 
    cp.matrix(c,tc="d"),
    cp.matrix(A,tc="d"),
    cp.matrix(b,tc='d')
)

print(sol["x"])
print(sol['primal objective'] + data['const'])

"""
Optimal solution found.
[ 7.50e-01]
[ 1.25e+00]

3.1249998233364806
"""