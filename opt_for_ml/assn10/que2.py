import numpy as np
import copy, sys
import pandas as pd

roll_no_last = 4

def calculate_f(x:np.array, weights:np.array, y:np.array) -> int:
    return ((np.dot(x,weights) - y)**2).sum() / (2 * x.shape[0])

def grad_f(x:np.array, weights:np.array, y:np.array) -> np.array:
    first_term = (x[:,:-1] * (np.dot(x,weights) - y)).sum()/ x.shape[0]
    second_term = (np.dot(x,weights) - y).sum() / x.shape[0]
    return np.array([[first_term],[second_term]],dtype=np.float64)

def return_dataset(x:np.array, y:np.array, batch_size:int):
    total_batches = int(x.shape[0] / batch_size)
    remaining_points = x.shape[0] - total_batches * batch_size
    for batch in range(total_batches):
        yield (x[batch:batch+batch_size],y[batch:batch+batch_size])
    if remaining_points != 0:
        yield (x[-remaining_points:],y[-remaining_points:])

def find_w(w_k:np.array, x:np.array, y:np.array, iteration:int) -> np.array:
    d_k = -grad_f(x, w_k, y)
    alpha = 1 / (iteration + 1)
    w_k = w_k + alpha * d_k
    return w_k

beta1 = 1e-4;
beta2 = 0.9;
epsilon = 0.001
r = 0.5
batch_size = 21
w_0 = np.array([[0],[0]], dtype=np.float64)

data = pd.read_excel(sys.argv[1])
data = np.array(data)
x = data[:,:-1]
y = data[:,-1:]
x = x / 1e3
y = y / 1e6
x = np.hstack([x,np.ones(x.shape)])
data_loader = return_dataset(x, y, batch_size)

iteration = 0
while calculate_f(x, w_0, y) > 0.93:
    for idx, (dx,dy) in enumerate(data_loader):
        cur_w = find_w(w_0, dx, dy, iteration)
        iteration += 1
        if calculate_f(x, cur_w, y) < 0.93:
            w_0 = cur_w
            break;
        if calculate_f(x, cur_w, y) < calculate_f(x, w_0, y):
            w_0 = cur_w
    if iteration == 5e5:
        break
    data_loader = return_dataset(x, y, batch_size)
print(w_0)
print(f"total_iterations: {iteration}")

print(calculate_f(x, w_0, y))

"""
[[0.57295871]
 [1.64604539]]
total_iterations: 500000
0.9408714950047855
"""