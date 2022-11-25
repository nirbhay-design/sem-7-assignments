import numpy as np
import copy

def calculate_f(x):
    r = 4;
    return (r - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2

def grad_f(x:np.array):
    h = 1e-5
    grad_vector = []
    cur_f = calculate_f(x)
    for i in range(x.shape[0]):
        x[i] += h
        new_f = calculate_f(x)
        x[i] -= h
        grad = (new_f - cur_f) / h
        grad_vector.append(grad)
    return np.array(grad_vector,dtype=np.float64).reshape(-1,1)

def check_armijo_wolf_cond(x_k: np.array, d_k: np.array, alpha:float, beta1:float, beta2:float) -> bool:
    xk_alp_dk = x_k + alpha * d_k;
    f_grad = grad_f(x_k);
    f_grad_alph = grad_f(xk_alp_dk)
    armijo_left = calculate_f(xk_alp_dk);
    armijo_right = calculate_f(x_k) + alpha * beta1 *np.dot(f_grad.T,d_k);

    wolf_left = np.dot(f_grad_alph.T, d_k)
    wolf_right = beta2 * np.dot(f_grad.T,d_k);

    return (armijo_left <= armijo_right) and (wolf_left >= wolf_right) 


def steepest_direction(x_k:np.array, d_k:np.array, beta1: float, beta2: float, r:float) -> float:
    alpha = 1;
    armijo_iter = 0
    while not check_armijo_wolf_cond(x_k, d_k, alpha, beta1, beta2):
        alpha = alpha * r
        armijo_iter += 1
        if armijo_iter == 50:
            break
    return alpha;

def cb(x_k, x_k_1):
    return np.linalg.norm(grad_f(x_k)) ** 2/ np.linalg.norm(grad_f(x_k_1)) ** 2

def find_x(x_0:np.array, beta1:float, beta2:float, epsilon:float, R:float) -> np.array:
    x_k = x_0
    d_k = -grad_f(x_k)
    norm_grad = np.linalg.norm(-d_k)
    iterations = 0
    while norm_grad > epsilon:
        alpha = steepest_direction(x_k, d_k, beta1, beta2, R);
        x_k_new = x_k + alpha * d_k
        d_k = -grad_f(x_k) + cb(x_k_new, x_k) * d_k
        x_k = x_k_new
        norm_grad = np.linalg.norm(grad_f(x_k))
        iterations += 1
        if iterations == 1000:
            break;
    return x_k, iterations

beta1 = 1e-4;
beta2 = 0.9;
epsilon = 0.001
R = 0.5
r = 4
x = np.array([[r+5],[r-5]],dtype=np.float64)
x, iterations = find_x(x, beta1, beta2, epsilon, R);

print(x)
print(iterations)


"""
[[ 3.98986937]
 [15.91904606]]
1000
"""



