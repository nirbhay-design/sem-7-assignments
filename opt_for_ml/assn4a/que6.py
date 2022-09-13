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

def complementary_slackness(x_star: np.array, A: np.array, b: np.array, lambd: np.array):
    A = A.astype(np.float64)
    ax_b = np.dot(A,x_star) - b;
    a = np.zeros((lambd.shape[0],lambd.shape[0]))
    np.fill_diagonal(a,lambd.reshape(lambd.shape[0]))
    comp_slack = np.dot(a,ax_b)
    return comp_slack

print(complementary_slackness(np.array(sol['x']),A,b,np.array(sol['z'])))

"""
Optimal solution found.
[ 5.00e-01]
[ 7.25e+00]

7.375000664251138
"""