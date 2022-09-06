import numpy as np
import pandas as pd
import cvxopt as cp
import json, sys

csv_file = sys.argv[1]
data = pd.read_csv(csv_file)
np_data = np.array(data)

def mean_return(np_data: np.array):
    # arr_1 = np.log(np_data[-1,:])
    # arr_0 = np.log(np_data[0,:])
    # return arr_1 - arr_0
    # return np.array(log_mean)

    log_mean = []
    ht, wd = np_data.shape
    for i in range(wd):
        stock_i = np_data[:,i]
        mean_i = 0
        for j in range(ht-1):
            ratio_return = stock_i[j+1]/stock_i[j]
            mean_i += np.log(ratio_return)
        log_mean.append(mean_i)
    return -np.array(log_mean)

def cov_matrix(np_data:np.array):
    np_data = np_data - np.mean(np_data,axis=0)
    return np.dot(np_data.T,np_data) / (np_data.shape[0] -1)

random_value = np.random.uniform(0.01,0.09)
Q= cov_matrix(np_data)
cov_matrix_shape = Q.shape[0]
c= np.zeros((cov_matrix_shape, 1))
A = np.vstack([mean_return(np_data), -np.eye(cov_matrix_shape)])
b = np.array([[-random_value]]+[[0] for _ in range(cov_matrix_shape)])
Aeq = np.array([[1 for _ in range(cov_matrix_shape)]])
beq = np.array([[1]])

sol = cp.solvers.qp(
    cp.matrix(Q,tc="d"), 
    cp.matrix(c,tc="d"),
    cp.matrix(A,tc="d"),
    cp.matrix(b,tc='d'),
    cp.matrix(Aeq,tc='d'),
    cp.matrix(beq,tc='d'),
)

print(sol["x"])
print(sol['primal objective'])
print(random_value)

"""
1
Optimal solution found.
[ 2.24e-01]
[ 2.56e-01]
[ 5.20e-01]

237.06700053009712
0.04849785118106109

2
Optimal solution found.
[ 6.68e-10]
[ 6.54e-11]
[ 7.06e-10]
[ 5.56e-01]
[ 4.44e-01]

13.088042848136974
0.017423491142073706

3
Optimal solution found.
[ 2.69e-09]
[ 4.60e-02]
[ 1.06e-09]
[ 4.31e-01]
[ 5.23e-01]

31.299801667223434
0.03722432234920744
"""