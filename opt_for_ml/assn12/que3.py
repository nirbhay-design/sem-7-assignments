from typing import final
import numpy as np

def grad_f(c, A, x, b, sigma):
    d = 1 / (np.dot(A,x)-b)
    value = A * d
    final_value = np.sum(value.T,axis=1) / sigma
    return c - final_value.reshape(-1,1)

def grad_2f(sigma, A, x, b):
    d = 1 / (np.dot(A,x)-b) ** 2
    final_value = None
    for idx, vector in enumerate(A):
        a_i = vector.reshape(-1,1)
        ai_ai_t = np.dot(a_i,a_i.T) / d[idx][0]
        if final_value is not None:
            final_value += ai_ai_t
        else:
            final_value = ai_ai_t
    return final_value




c = np.array([[-20],[-12],[-40],[-25]],dtype=np.float64)
A = np.array([[1,1,1,1],[3,2,1,0],[0,1,2,3],[-1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,-1]],dtype=np.float64)
b = np.array([[50],[100],[90],[0],[0],[0],[0]],dtype=np.float64)
x_0 = np.array([[1],[1],[1],[1]],dtype=np.float64)
m = 6
sigma = 1
R = 2
epsilon = 1e-3

iteration = 0

while True:
    iteration += 1
    gradf = grad_f(c, A, x_0, b, sigma)
    hessian = grad_2f(sigma, A, x_0, b)
    x_0 = x_0 - np.linalg.inv(hessian) @ gradf
    sigma = sigma * R
    if m / sigma < epsilon:
        break

print(iteration)

print(x_0)