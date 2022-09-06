import numpy as np
import pandas as pd
import cvxopt as cp

# c=np.array([[-5.0],[-7.0]])
# A=np.array([[1,1],[3,8],[10,7],[-1,0],[0,-1]])
# b=np.array([[4],[24],[35],[0],[0]])

# c = np.array([[30],[20]])
# A = np.array([[-5,-1],[-2,-2],[-1,-4],[-1,0],[0,-1]])
# b = np.array([[-10],[-12],[-12],[0],[0]])

c = np.array([[30],[20],[40],[25],[10]])
A = np.array([[2,1,3,3,1],[3,2,2,1,1],[-1,0,0,0,0],[0,-1,0,0,0],[0,0,-1,0,0],[0,0,0,-1,0],[0,0,0,0,-1]])
b = np.array([[700],[1000],[0],[0],[0],[0],[0]])

def print_cp(*array):
    for arr in array:
        print(arr.shape, cp.matrix(arr))

sol =cp.solvers.lp(cp.matrix(c,tc="d"), cp.matrix(A,tc="d"),cp.matrix(b,tc="d"))
print(sol["x"],sol["primal objective"])

