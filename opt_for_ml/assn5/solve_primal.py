import numpy as np
import pandas as pd
import cvxopt as cp
import json, sys
import matplotlib.pyplot as plt

csv_file = sys.argv[1]
csv_data = pd.read_csv(csv_file)

target_file = sys.argv[2]
target_data = pd.read_csv(target_file)

csv_data = np.array(csv_data)
target_data = np.array(target_data)
target_data[target_data == 0] = -1

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

def plot_line(csv_data, W, target_data,L, save_path):
    new_csv_data = np.hstack([csv_data,L])
    new_csv_data = new_csv_data[new_csv_data[:,-1] != 0]
    new_x1 = new_csv_data[:,0]
    new_x2 = new_csv_data[:,1]
    csv_data = np.hstack([csv_data, target_data])
    w1, w2, b = W.reshape(W.shape[0])
    x1 = csv_data[:,0]
    # x-> x1, y-> x2
    x2_values = (-w1 * x1 - b)/w2
    x2_values_1 = (-w1 * x1 - b - 1)/w2
    x2_values_2 = (-w1 * x1 - b + 1)/w2
    x11 = csv_data[csv_data[:,2] == 1]
    x12 = csv_data[csv_data[:,2] == -1]
    plt.figure(figsize=(5,4))
    plt.scatter(x11[:,0],x11[:,1],color='blue', label='+1')
    plt.scatter(x12[:,0],x12[:,1],color='purple',label='-1')
    plt.plot(x1,x2_values,color='red')
    plt.plot(x1,x2_values_1,color='green')
    plt.plot(x1,x2_values_2,color='green')
    plt.scatter(new_x1,new_x2,color='black')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend()
    plt.savefig(save_path)    
 

w_b = np.array(sol["x"])
# w2 = w_b[1]
# w_b[1] = w_b[0]
# w_b[0] = w2

plot_line(csv_data, w_b, target_data, L, sys.argv[3])

"""
Optimal solution found.
[ 2.88e-01]
[ 3.33e-01]
[ 1.63e+00]

Optimal solution found.
[-9.40e-03]
[ 4.29e-01]
[-4.47e-01]

Optimal solution found.
[-2.43e-01]
[ 5.29e-01]
[ 2.81e+00]
"""