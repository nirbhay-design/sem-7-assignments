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
 0:  4.7705e+00  4.7705e+00  5e+00  8e-01  0e+00  1e+00
 1:  6.3834e+00  6.5666e+00  1e+00  2e-01  4e-16  4e-01
 2:  7.4553e+00  7.4689e+00  8e-02  1e-02  5e-15  3e-02
 3:  7.4995e+00  7.4997e+00  8e-04  1e-04  1e-15  3e-04
 4:  7.5000e+00  7.5000e+00  8e-06  1e-06  0e+00  3e-06
 5:  7.5000e+00  7.5000e+00  8e-08  1e-08  1e-15  3e-08
Optimal solution found.
[ 1.25e+00]
[-2.47e-09]
 7.499999954272108
dual solution
     pcost       dcost       gap    pres   dres   k/t
 0: -4.7705e+00 -1.1262e+01  5e+00  0e+00  4e-01  1e+00
 1: -6.5666e+00 -7.9853e+00  1e+00  4e-16  1e-01  4e-01
 2: -7.4689e+00 -7.5516e+00  8e-02  2e-16  6e-03  3e-02
 3: -7.4997e+00 -7.5005e+00  8e-04  4e-17  6e-05  3e-04
 4: -7.5000e+00 -7.5000e+00  8e-06  2e-16  6e-07  3e-06
 5: -7.5000e+00 -7.5000e+00  8e-08  2e-16  6e-09  3e-08
Optimal solution found.
[ 2.22e-09]
[ 1.50e+00]
 -7.499999968071891
"""