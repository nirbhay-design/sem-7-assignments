import numpy as np
import copy, sys, random
import pandas as pd

roll_no_last = 4

class dataset:
    def __init__(self, x:np.array, y:np.array, batch_size:int):
        self.x = x
        self.y = y
        self.bs = batch_size
        self.batch_index = 0
        self.no_batch = x.shape[0] // batch_size + (0 if x.shape[0] % batch_size == 0 else 1)
        print(f"Total number of batches: {self.no_batch}")

    def __next__(self):
        cur_dataset = (self.x[self.batch_index * self.bs: (self.batch_index + 1) * self.bs], self.y[self.batch_index * self.bs: (self.batch_index + 1) * self.bs])
        self.batch_index = (self.batch_index + 1) % self.no_batch
        return cur_dataset

def calculate_f(x:np.array, weights:np.array, y:np.array) -> int:
    return ((np.dot(x,weights) - y)**2).sum() / (2 * x.shape[0])

def grad_f(x:np.array, weights:np.array, y:np.array) -> np.array:
    common_term = np.dot(x,weights) - y # N x 1, x: N x 5
    gradient = np.dot(x.T, common_term) # 5 x 1
    gradient = gradient / x.shape[0]
    return gradient

def find_w(w_k:np.array, x:np.array, y:np.array, iteration:int) -> np.array:
    d_k = -grad_f(x, w_k, y)
    alpha = 1 / (iteration + 1)
    w_k = w_k + alpha * d_k
    return w_k

beta1 = 1e-4;
beta2 = 0.9;
epsilon = 0.001
r = 0.5
batch_size = 10

data = pd.read_excel(sys.argv[1])
data = np.array(data)
x = data[:,:-1]
y = data[:,-1:]
x = x.astype(np.float64)
y = y.astype(np.float64)
x = x/1e2
y = y/1e3
w_0 = np.array([[0] for _ in range(data.shape[1]-1)], dtype=np.float64)
data_loader = list(zip(x,y))

iteration = 0
while True:
    random_samples = random.sample(data_loader, batch_size)
    dx,dy = zip(*random_samples)
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

R = 14
r = 4
new_input = np.array([[R + r/10],[100 + R + 2*r/10],[R-1 + r/10],[54.3],[r + R/100]]).reshape(1,-1)
print(new_input)
new_input = new_input / 1e2
print('output on sample input')
print(np.dot(new_input,w_0) * 1e3)

"""
weight values
[[2.82781254]
 [5.12214926]
 [1.70893591]
 [1.32076932]
 [0.09105886]]
total_iterations: 100
[[ 14.4  114.8   13.4   54.3    4.14]]
output on sample input
[[7237.37734854]]
"""