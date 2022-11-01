import numpy as np
import warnings
warnings.filterwarnings("ignore")

def calculate_f(x:np.array):
    f_val = x[0] ** 2 + x[1] ** 2 + 2 * (x[2] ** 2) + x[3] ** 2 - 5 * x[0] - 5 * x[1] - 21 * x[2] + 7 * x[3]
    return f_val

def calculate_g1(x:np.array):
    g1_value = x[0] ** 2 + x[1] ** 2 + x[2] ** 2 + x[3] ** 2 + x[0] - x[1] + x[2] - x[3] - 8
    return g1_value

def calculate_g2(x:np.array):
    g2_value = x[0] ** 2 + 2 * (x[1] ** 2) + x[2] ** 2 + 2 * (x[3] ** 2) - x[0] - x[3] - 10
    return g2_value

def grad_f(cal_f:callable, x:np.array):
    """
    x: shape(N+1,1)
    """

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

grad_1 = lambda x: (2 * x[0] + 1) / calculate_g1(x)
grad_2 = lambda x: (2 * x[1] - 1) / calculate_g1(x)
grad_3 = lambda x: (2 * x[2] + 1) / calculate_g1(x)
grad_4 = lambda x: (2 * x[3] - 1) / calculate_g1(x)

grad_5 = lambda x: (2 * x[0] - 1) / calculate_g2(x)
grad_6 = lambda x: (4 * x[1]) / calculate_g2(x)
grad_7 = lambda x: (2 * x[2]) / calculate_g2(x)
grad_8 = lambda x: (4 * x[3] - 1) / calculate_g2(x)

def grad_lag(x, sigma):
    x = x.reshape(-1)
    first_term = np.array([[2*x[0]-5],[2*x[1]-5],[4*x[2]-21],[2*x[3]+7]],dtype=np.float64)
    second_term = np.array([[grad_1(x)],[grad_2(x)],[grad_3(x)],[grad_4(x)]],dtype=np.float64)
    third_term = np.array([[grad_5(x)],[grad_6(x)],[grad_7(x)],[grad_8(x)]],dtype=np.float64)
    
    return first_term + (second_term + third_term) / sigma


def jacobian_lag(x, sigma):
    first_term = np.zeros((x.shape[0],x.shape[0]),dtype=np.float64)
    np.fill_diagonal(first_term,np.array([2,2,4,2],dtype=np.float64))
    
    second_term = np.vstack([grad_f(grad_1,x).T,grad_f(grad_2,x).T,grad_f(grad_3,x).T,grad_f(grad_4,x).T])
    third_term = np.vstack([grad_f(grad_5,x).T,grad_f(grad_6,x).T,grad_f(grad_7,x).T,grad_f(grad_8,x).T])

    return first_term + (second_term + third_term) / sigma

def find_x(x, sigma, m, R):
    while (m/sigma > 1e-4):
        jaco_inv = np.linalg.inv(jacobian_lag(x, sigma))
        F = grad_lag(x, sigma)
        x = x - jaco_inv @ F 
        sigma *= R
    return x

x = np.array([[1],[1],[1],[1]],dtype=np.float64)
m = 1
sigma = 1   
R = 10
print(find_x(x, sigma, m ,R))

"""
optmial x:

[[ 2.4999111 ]
 [ 2.49988142]
 [ 5.24990335]
 [-3.49980328]]
"""