import numpy as np
import random
import sys

f1 = lambda x: x[0] ** 2 + x[1] ** 2 -2
f2 = lambda x: np.exp(x[0]-1) + x[1] ** 3 -2

def calculate_fxu(x:np.array):
    return np.vstack([f1(x),f2(x)])

def jacobian(x:np.array):
    frv = 2*x[0]
    sv = 2*x[1]
    tv = np.exp(x[0] - 1)
    fv = 3 * (x[1] ** 2)
    return np.vstack([np.hstack([frv,sv]),np.hstack([tv,fv])])

def break_criteria(x_k, condition):
    cond = calculate_fxu(x_k)
    return np.linalg.norm(cond) < condition

def cal_solution(x_k:np.array, condition):
    iteration = 0
    while True:
        if break_criteria(x_k, condition):
            break
        iteration += 1
        jac = jacobian(x_k)
        jac_inv = np.linalg.inv(jac)
        f_xu = calculate_fxu(x_k)
        update_value = np.dot(jac_inv,f_xu)
        x_k = x_k - update_value
        if iteration == 1000:
            break
    return x_k, iteration


x = np.array([[2],[3]],dtype=np.float64)
condition=1e-4
x_k, iteration = cal_solution(x, condition)
print(x_k)
print(iteration)


"""
[[0.99999872]
 [1.00000267]]
6
"""