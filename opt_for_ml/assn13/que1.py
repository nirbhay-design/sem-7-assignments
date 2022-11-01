import numpy as np
import warnings
warnings.filterwarnings("ignore")

def grad_f(x:np.array):
    return np.array([[200*(x[0] - 1)],[1]],dtype=np.float64)

def grad_2f(x:np.array):
    return np.array([[200,0],[0,0]],dtype=np.float64)

def calculate_F(x:np.array, A:np.array, b:np.array, mu:np.array):
    first_term = grad_f(x) + A.T @ mu
    second_term = A @ x - b
    return np.vstack([first_term,second_term])

def jacobian_F(x:np.array, A:np.array, b:np.array, mu:np.array):
    first_term = np.hstack([grad_2f(x), A.T])
    second_term = np.hstack([A,np.zeros((A.shape[0],A.shape[0]),dtype=np.float64)])
    return np.vstack([first_term, second_term])    

def find_x(x:np.array, mu:np.array, A:np.array, b:np.array):
    iteration = 0
    while True:
        final_feature = np.vstack([x,mu])
        iteration += 1
        jac_inv = np.linalg.inv(jacobian_F(x, A, b, mu))
        f_value = calculate_F(x, A, b, mu)
        final_feature = final_feature - jac_inv @ f_value
        x = final_feature[:x.shape[0],:]
        mu = final_feature[x.shape[0]:,:]
        if iteration == 1000:
            break
    return x, mu 

x = np.array([[1],[1]],dtype=np.float64)
mu = np.array([[1],[1]],dtype=np.float64)
A = np.array([[1,6],[-4,1]],dtype=np.float64)
b = np.array([[36],[0]],dtype=np.float64)

final_x, final_mu = find_x(x, mu, A, b)
print(final_x)
print(final_mu)

"""
optimal x
[[1.44]
 [5.76]]
optimal mu
[[-3.68]
 [21.08]]
"""