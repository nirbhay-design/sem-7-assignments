import numpy as np
import copy, sys
import pandas as pd

roll_no_last = 4

def calculate_f(x:np.array, weights:np.array, y:np.array) -> int:
    return ((np.dot(x,weights) - y)**2).sum() / (2 * x.shape[0])

def grad_f(x:np.array, weights:np.array, y:np.array) -> np.array:
    common_term = np.dot(x,weights) - y # N x 1, x: N x 5
    gradient = np.dot(x.T, common_term) # 5 x 1
    gradient = gradient / x.shape[0]
    return gradient

def check_armijo_wolf_cond(w_k: np.array, d_k: np.array, x:np.array, y:np.array, alpha:float, beta1:float, beta2:float) -> bool:
    xk_alp_dk = w_k + alpha * d_k;
    f_grad = grad_f(x, w_k, y);
    f_grad_alph = grad_f(x, xk_alp_dk, y)

    armijo_left = calculate_f(x, xk_alp_dk, y);
    armijo_right = calculate_f(x, w_k, y) + alpha * beta1 *np.dot(f_grad.T,d_k);

    wolf_left = np.dot(f_grad_alph.T, d_k)
    wolf_right = beta2 * np.dot(f_grad.T,d_k);

    return (armijo_left <= armijo_right) and (wolf_left >= wolf_right) 


def steepest_direction(w_k:np.array, d_k:np.array, x:np.array, y:np.array, beta1: float, beta2: float, r:float) -> float:
    alpha = 1;
    while not check_armijo_wolf_cond(w_k, d_k, x, y, alpha, beta1, beta2):
        alpha = alpha * r
    return alpha;

def find_w(w_0:np.array, x:np.array, y:np.array, beta1:float, beta2:float, epsilon:float, r:float) -> np.array:
    w_k = w_0
    d_k = -grad_f(x, w_k, y)
    norm_grad = np.linalg.norm(-d_k)

    iterations = 0
    while norm_grad > epsilon:
        alpha = steepest_direction(w_k, d_k, x, y, beta1, beta2, r);
        w_k = w_k + alpha * d_k
        d_k = -grad_f(x, w_k, y)
        norm_grad = np.linalg.norm(-d_k)
        iterations += 1
        if iterations == 2000:
            break;
    return w_k, iterations


beta1 = 1e-4;
beta2 = 0.9;
epsilon = 0.01
r = 0.5

data = pd.read_excel(sys.argv[1])
data = np.array(data)
w_0 = np.array([[0] for _ in range(data.shape[1]-1)], dtype=np.float64)
x = data[:,:-1]
y = data[:,-1:]
print(x.shape, y.shape)
w, iterations = find_w(w_0, x, y, beta1, beta2, epsilon, r)


# print('\n')
print("weight values")
print(w)

print(f"total_iterations: {iterations}")
# print(f"final objective function value: {calculate_f(x,w,y)}")

R = 14
r = 4

new_input = np.array([[R + r/10],[100 + R + 2*r/10],[R-1 + r/10],[54.3],[r + R/100]]).reshape(1,-1)
print(new_input)
print("output for new input")
print(np.dot(new_input,w))

"""
(205, 5) (205, 1)
weight values
[[-107.39959718]
 [ 470.7610122 ]
 [-272.51752862]
 [-745.75614296]
 [  15.32276041]]
total_iterations: 2000
[[ 14.4  114.8   13.4   54.3    4.14]]
output for new input
[[8413.95278305]]
"""