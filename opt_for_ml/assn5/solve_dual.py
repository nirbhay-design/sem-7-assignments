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

N, n_features = csv_data.shape

Y = np.zeros((N,N))
np.fill_diagonal(Y,target_data)
Q = np.dot(np.dot(Y,csv_data),np.dot(csv_data.T,Y))
c = -np.ones((N,1))
A = -np.eye(N)
b = np.zeros((N,1))
Aeq = target_data.T
beq = np.array([[0]])

# print(Q.shape, c.shape, Aeq.shape, beq.shape, A.shape, b.shape)

# print(Aeq)
# print(beq)
# print(c)
# print(Q)

sol = cp.solvers.qp(
    P = cp.matrix(Q,tc="d"), 
    q = cp.matrix(c,tc="d"),
    G = cp.matrix(A,tc="d"),
    h = cp.matrix(b,tc='d'),
    A = cp.matrix(Aeq,tc='d'),
    b = cp.matrix(beq,tc='d'),
)

print(sol["x"])
print(sol['primal objective'])


def calculate_w(X, Y, L):
    return np.dot((X*Y).T,L)

def calculate_b(W, X, Y, L):
    N_X = np.hstack([X,Y,L])
    N_X = N_X[N_X[:,-1] != 0]
    X = N_X[:,:-2]
    Y = N_X[:,-2:-1]
    b = Y - np.dot(X,W)
    return round(b[0][0],2)

L = np.array(sol['x'])
L = np.array(list(map(lambda x: round(x[0],5),L))).reshape(-1,1)

print(L)

W = calculate_w(csv_data, target_data, L)

B = calculate_b(W, csv_data, target_data, L)

w_b = np.vstack([W,np.array([[B]])])

print(w_b)

def plot_line(csv_data, W, target_data, L, save_path):
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
    plt.scatter(new_x1,new_x2,color='black')
    plt.plot(x1,x2_values,color='red')
    plt.plot(x1,x2_values_1,color='green')
    plt.plot(x1,x2_values_2,color='green')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend()
    plt.savefig(save_path)    

plot_line(csv_data, w_b, target_data, L, sys.argv[3])

"""
[[0.28846684]
 [0.33336018]
 [1.63      ]]

[[-0.00941362]
 [ 0.42868884]
 [-0.45      ]]

[[-0.24313389]
 [ 0.52886723]
 [ 2.81      ]]
"""
