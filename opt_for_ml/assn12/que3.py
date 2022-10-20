import numpy as np

def grad_f(c, A, x, b, sigma):
    d = 1 / (b - np.dot(A,x))
    value = A * d
    final_value = np.sum(value.T,axis=1) / sigma
    return c + final_value.reshape(-1,1)

def grad_2f(sigma, A, x, b):
    d = 1 / (b - np.dot(A,x)) ** 2
    value = A ** 2
    final_value = np.sum(value.T, d) / sigma
    return final_value

c = np.array([[-20],[-12],[-40],[-25]],dtype=np.float64)
A = np.array([[1,1,1,1],[3,2,1,0],[0,1,2,3],[-1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,-1]],dtype=np.float64)
b = np.array([[50],[100],[90],[0],[0],[0],[0]],dtype=np.float64)
x_0 = np.array([[1],[1],[1],[1]],dtype=np.float64)
m = 6
sigma = 1
R = 10
epsilon = 1e-3

print(grad_f(c, A, x_0, b, sigma))