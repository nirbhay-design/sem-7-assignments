import numpy as np
import pandas as pd
import cvxopt as cp
import json, sys
import matplotlib.pyplot as plt

csv_file = sys.argv[1]
csv_data = pd.read_csv(csv_file)

whole_data = np.array(csv_data)
csv_data = whole_data[:,:-1]
target_data = whole_data[:,-1:]

n_features = csv_data.shape[1]
Q=np.eye(n_features+1)
Q[n_features][n_features] = 0
c=np.zeros((n_features+1,1))

A = -np.hstack([csv_data * target_data, target_data])
b = -np.ones((csv_data.shape[0],1))

sol = cp.solvers.qp(
    cp.matrix(Q,tc="d"), 
    cp.matrix(c,tc="d"),
    cp.matrix(A,tc="d"),
    cp.matrix(b,tc='d')
)

print(sol["x"])
print(sol['primal objective'])

L = np.array(sol['z'])
L = np.array(list(map(lambda x: round(x[0],5),L))).reshape(-1,1) 

w_b = np.array(sol["x"])


"""
Optimal solution found.
[ 1.35e-01]
[-3.44e-01]
[-3.88e-01]
[ 2.01e-02]
[ 1.97e+00]

0.14376280379907244
"""

