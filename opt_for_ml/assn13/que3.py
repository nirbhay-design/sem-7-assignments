import numpy as np
import warnings
warnings.filterwarnings("ignore")

f_grad_one = lambda x: np.exp(x[0]) * (4 * x[0] ** 2 + 2 * x[1] ** 2 + 4 * x[0] * x[1] + 8 * x[0] + 6 * x[1] + 1)
f_grad_two = lambda x: np.exp(x[0]) * (4 * x[0] + 4 * x[1] + 2)

log_grad_one = lambda x: x[0] / (25 - x[0] ** 2 - x[1] ** 2)
log_grad_two = lambda x: x[1] / (25 - x[0] ** 2 - x[1] ** 2)

def grad_fun(cal_f:callable, x:np.array):
    h = 1e-5
    grad_vector = []
    cur_f = cal_f(x)
    for i in range(x.shape[0]):
        x[i] += h
        new_f = cal_f(x)
        x[i] -= h
        grad = (new_f - cur_f) / h
        grad_vector.append(grad)
    return np.array(grad_vector,dtype=np.float64).reshape(-1,1)

def Lagrange(x, A, b, mu, sigma):
    return np.exp(x[0]) * (4 * x[0] ** 2 + 2 * x[1] ** 2 + 4 * x[0] * x[1] + 2 * x[1] + 1) - 1/sigma * (np.log(25 - x[0] ** 2 - x[1] ** 2)) + mu.T @ (A @ x - b)

def grad_Lag(x, A, b, mu, sigma):
    grad_f_first = f_grad_one(x)
    grad_f_second = f_grad_two(x)
    final_grad_f = np.vstack([grad_f_first, grad_f_second])

    grad_log_first = log_grad_one(x)
    grad_log_second = log_grad_two(x)
    final_grad_log = np.vstack([grad_log_first, grad_log_second])
    final_grad_log = final_grad_log * (2/sigma)

    linear_grad = A.T @ mu
    lag_grad_x = final_grad_f + final_grad_log + linear_grad
    lag_grad_mu = A @ x - b
    return np.vstack([lag_grad_x, lag_grad_mu])

def jacobian_lag(x, A, sigma):
    H1 = np.vstack([grad_fun(f_grad_one, x).T, grad_fun(f_grad_two, x).T])
    H2 = np.vstack([grad_fun(log_grad_one,x).T,grad_fun(log_grad_two,x).T])
    return np.vstack([np.hstack([H1 + 1/sigma * H2, A.T]), np.hstack([A,np.zeros((A.shape[0],A.shape[0]),dtype=np.float64)])]) 

def find_x(x, A, b, mu, sigma, m, R):
    while (m/sigma > 1e-4):
        feature = np.vstack([x,mu])
        jaco_inv = np.linalg.inv(jacobian_lag(x, A, sigma))
        F = grad_Lag(x, A, b, mu, sigma)
        feature = feature - jaco_inv @ F 
        x = feature[:x.shape[0],:]
        mu = feature[x.shape[0]:,:]
        sigma *= R
    return x, mu

x = np.array([[1],[1]],dtype=np.float64) 
A = np.array([[1,2]],dtype=np.float64)
mu = np.array([[1]],dtype=np.float64)
b = np.array([[5]],dtype=np.float64)
m = 1
sigma = 1   
R = 10
# print(jacobian_lag(x, A ,sigma))
# print(grad_Lag(x, A, b, mu, sigma))
x, mu = find_x(x, A, b, mu, sigma, m, R)
print(x)
print(mu)

"""
optimal x
[[-2.37443567]
 [ 3.68721783]]
 optimal mu
[[0.10197661]]
"""