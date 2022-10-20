import numpy as np
import copy, sys, random
import pandas as pd

roll_no_last = 4

def calculate_f(x:np.array, weights:np.array, y:np.array) -> int:
    """
    x.shape = (N,1)
    w.shape = (3,1)
    """
    x = np.hstack([x**2, x, np.ones((x.shape[0],1),dtype=np.float64)])
    return ((np.dot(x,weights) - y)**2).sum() / (2 * x.shape[0])

def grad_f(x:np.array, weights:np.array, y:np.array) -> np.array:
    new_x = np.hstack([x**2, x, np.ones((x.shape[0],1),dtype=np.float64)])
    common_term = np.dot(new_x,weights) - y
    grads = np.dot(new_x.T, common_term)
    grads = grads / y.shape[0]
    return grads

def find_w(w_k:np.array, x:np.array, y:np.array, iteration:int) -> np.array:
    d_k = -grad_f(x, w_k, y)
    alpha = 1 / (iteration + 1)
    w_k = w_k + alpha * d_k
    return w_k

batch_size = 20

data = pd.read_csv(sys.argv[1])
data = np.array(data)
x = data[:,:-1]
y = data[:,-1:]
x = x / 1e3
y = y / 1e6
w_0 = np.array([[0] for _ in range(2*x.shape[1] + 1)], dtype=np.float64)
data_loader = list(zip(x,y))

iteration = 0
while True:
    data = random.sample(data_loader, batch_size)
    dx,dy = zip(*data)
    dx = np.vstack(dx)
    dy = np.vstack(dy)
    cur_w = find_w(w_0, dx, dy, iteration)
    iteration += 1
    if calculate_f(x, cur_w, y) < calculate_f(x, w_0, y):
        w_0 = cur_w
    if iteration == 100:
        break
print("weight values")
print(w_0)
print(f"total_iterations: {iteration}")

print(f"objective function value {calculate_f(x, w_0, y)}")

"""
weight values
[[2.09461615e-06]
 [2.14663145e-07]
 [1.99289825e-08]
 [2.09493519e-07]
 [2.35191377e-09]
 [6.86626558e-06]
 [5.93245427e-06]
 [4.05981082e-07]
 [4.94062729e-06]
 [1.38726089e-06]
 [2.45857463e-07]
 [1.41617772e-06]
 [1.70268829e-07]
 [8.20296830e-06]
 [7.53024647e-06]
 [2.21742784e-06]
 [9.68303089e-06]]
total_iterations: 100
objective function value 1.4292393913900596e-10
"""