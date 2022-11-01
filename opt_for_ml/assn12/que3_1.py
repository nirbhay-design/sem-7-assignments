from typing import final
import numpy as np

import warnings
warnings.filterwarnings("ignore")

n = 2;
beta1 = 1e-4;
beta2 = 0.9;
# epsilon = 0.001
r = 0.5
c = np.array([[-20],[-12],[-40],[-25]],dtype=np.float64)
A = np.array([[1,1,1,1],[3,2,1,0],[0,1,2,3],[-1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,-1]],dtype=np.float64)
b = np.array([[50],[100],[90],[0],[0],[0],[0]],dtype=np.float64)
x_0 = np.array([[1/10],[1/10],[1/10],[1/10]],dtype=np.float64)
B = np.eye(4,dtype=np.float64)
m = 6
sigma = 1
R = 2
epsilon = 1e-3

def calculate_f(c, A, x, b, sigma):
    summation_term = np.sum(np.log(b-A@x))
    return c.T @ x - (1/sigma) * summation_term

def grad_f(c, A, x, b, sigma):
    d = 1 / (np.dot(A,x)-b)
    value = A * d
    final_value = np.sum(value.T,axis=1) / sigma
    return c - final_value.reshape(-1,1)

def check_armijo_wolf_cond(x_k: np.array, d_k: np.array, alpha:float, beta1:float, beta2:float, sigma:int) -> bool:
    xk_alp_dk = x_k + alpha * d_k;
    f_grad = grad_f(c, A, x_k, b, sigma);
    f_grad_alph = grad_f(c, A, xk_alp_dk, b, sigma)
    armijo_left = calculate_f(c, A, xk_alp_dk, b, sigma);
    armijo_right = calculate_f(c, A, x_k, b, sigma) + alpha * beta1 *np.dot(f_grad.T,d_k);

    wolf_left = np.dot(f_grad_alph.T, d_k)
    wolf_right = beta2 * np.dot(f_grad.T,d_k);

    return (armijo_left <= armijo_right) and (wolf_left >= wolf_right) 


def steepest_direction(x_k:np.array, d_k:np.array, beta1: float, beta2: float, r:float, sigma:int) -> float:
    alpha = 1;
    while not check_armijo_wolf_cond(x_k, d_k, alpha, beta1, beta2, sigma):
        alpha = alpha * r
        if alpha < 1e-4:
            break
    return alpha;

def find_x(x_0:np.array, B:np.array, beta1:float, beta2:float, sigma:int, epsilon:float, r:float, R:int) -> np.array:
    x_k = x_0
    d_k = -np.dot(B,grad_f(c, A, x_k, b, sigma))
    norm_grad = np.linalg.norm(-d_k)

    iterations = 0
    while norm_grad > epsilon:
        alpha = steepest_direction(x_k, d_k, beta1, beta2, r, sigma);
        x_k = x_k + alpha * d_k
        d_k = -np.dot(B,grad_f(c, A, x_k, b, sigma))
        sigma = sigma * R
        norm_grad = np.linalg.norm(-d_k)
        iterations += 1
        if iterations == 1000 or (m/sigma < epsilon):
            break;
    return x_k, iterations

x_k, iterations = find_x(x_0, B, beta1, beta2, sigma, epsilon, r, R)

print(x_k)

print(iterations)
