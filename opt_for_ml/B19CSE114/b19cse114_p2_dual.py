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

N, n_features = csv_data.shape

Y = np.zeros((N,N))
np.fill_diagonal(Y,target_data)
Q = np.dot(np.dot(Y,csv_data),np.dot(csv_data.T,Y))
c = -np.ones((N,1))
A = -np.eye(N)
b = np.zeros((N,1))
Aeq = target_data.T
beq = np.array([[0]])

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

"""
[[ 0.13528242]
 [-0.34416064]
 [-0.38775379]
 [ 0.02033715]
 [ 1.97      ]]
"""