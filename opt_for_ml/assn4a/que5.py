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

print(sol['z'])
"""
Optimal solution found.
[ 2.50e+00]
[ 6.79e-09]

-11.249999952471065
"""