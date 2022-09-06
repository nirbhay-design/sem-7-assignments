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
Aeq = np.array(data['Aeq'])
beq = np.array(data['beq'])

sol = cp.solvers.qp(
    cp.matrix(Q,tc="d"), 
    cp.matrix(c,tc="d"),
    cp.matrix(A,tc="d"),
    cp.matrix(b,tc='d'),
    cp.matrix(Aeq,tc='d'),
    cp.matrix(beq,tc='d')
)

print(sol["x"])
print(sol['primal objective'] + data['const'])

"""
Optimal solution found.
[ 5.00e-01]
[ 5.67e-04]
[ 5.00e-01]

0.5000001605670136
"""