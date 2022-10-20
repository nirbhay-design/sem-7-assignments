import numpy as np
import copy, sys
import pandas as pd

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
        if iterations == 1000:
            break;
    return w_k, iterations


beta1 = 1e-4;
beta2 = 0.9;
epsilon = 0.01
r = 0.5

data = pd.read_csv(sys.argv[1])
data = np.array(data)
x = data[:,:-1]
y = data[:,-1:]
x = x / 1e2
y = y / 1e2
w_0 = np.array([[0] for _ in range(2*x.shape[1] + 1)], dtype=np.float64)
w, iterations = find_w(w_0, x, y, beta1, beta2, epsilon, r)

# print('\n')
print("weight values")
print(w)

print(f"total_iterations: {iterations}")

print(f"objective function value: {calculate_f(x, w, y)}")


"""
weight values
[[ 1.43123329e-02]
 [ 1.06933490e-02]
 [ 2.74550002e-03]
 [-1.53774443e-03]
 [ 7.43829578e-05]
 [ 5.01807844e-04]
 [ 1.43165190e-03]
 [ 6.07989622e-03]
 [ 3.80186701e-03]
 [ 6.51654657e-03]
 [ 2.29182350e-03]
 [ 1.45989026e-04]
 [ 5.89108817e-04]
 [ 3.54756960e-03]
 [ 2.92014144e-03]
 [ 5.07208941e-03]
 [ 7.27987673e-04]]
total_iterations: 1000
objective function value: 0.009841334196678
"""