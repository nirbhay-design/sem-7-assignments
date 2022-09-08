import numpy as np
import pandas as pd
import cvxopt as cp
import json, sys

json_file = sys.argv[1]
with open(json_file, 'r') as jf:
    data = json.load(jf)

c=np.array(data["primal"]['c'])
A=np.array(data["primal"]['A'])
b=np.array(data["primal"]['b'])

print(f"primal solution")

sol = cp.solvers.lp(
    cp.matrix(c,tc="d"), 
    cp.matrix(A,tc="d"),
    cp.matrix(b,tc="d"),
    solver=data["primal"]['solvers'],
    verbose=False)


print(sol["x"],sol["primal objective"])

c_dual=np.array(data["dual"]['c'])
A_dual=np.array(data["dual"]['A'])
b_dual=np.array(data["dual"]['b'])

print("dual solution")

sol_dual = cp.solvers.lp(
    cp.matrix(c_dual,tc="d"), 
    cp.matrix(A_dual,tc="d"),
    cp.matrix(b_dual,tc="d"),
    solver=data["dual"]['solvers'],
    verbose=False)


print(sol_dual["x"],sol_dual["primal objective"])

"""
primal solution
     pcost       dcost       gap    pres   dres   k/t
 0:  5.6667e+00 -7.6667e+00  1e+01  0e+00  8e-01  1e+00
 1: -3.0903e+00 -7.2531e+00  7e+00  3e-16  3e-01  1e+00
 2: -5.0300e+00 -5.3779e+00  1e+00  3e-16  4e-02  3e-01
 3: -5.9888e+00 -5.9925e+00  2e-02  5e-16  6e-04  7e-03
 4: -5.9999e+00 -5.9999e+00  2e-04  2e-16  6e-06  7e-05
 5: -6.0000e+00 -6.0000e+00  2e-06  3e-16  6e-08  7e-07
Optimal solution found.
[ 2.62e-08]
[ 6.00e+00]
 -5.999998877961404
dual solution
     pcost       dcost       gap    pres   dres   k/t
 0: -5.6667e+00 -5.6667e+00  1e+01  2e+00  2e-16  1e+00
 1:  2.0326e+00  3.0903e+00  7e+00  7e-01  4e-16  1e+00
 2:  4.7480e+00  5.0300e+00  1e+00  8e-02  4e-16  3e-01
 3:  5.9822e+00  5.9888e+00  2e-02  1e-03  3e-15  7e-03
 4:  5.9998e+00  5.9999e+00  2e-04  1e-05  9e-16  7e-05
 5:  6.0000e+00  6.0000e+00  2e-06  1e-07  8e-16  7e-07
 6:  6.0000e+00  6.0000e+00  2e-08  1e-09  6e-16  7e-09
Optimal solution found.
[ 1.00e+00]
[-1.59e-09]
 5.999999982201881
"""