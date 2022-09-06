import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

class Config:
    xl_path = sys.argv[1]
    sample_input = np.array([4000])

config = Config()

def polynomial_matrix(x: np.array, degree):
    arr = []
    for i in range(degree,-1,-1):
        val = x ** i
        val = val.reshape((val.shape[0],1))
        arr.append(val)
    return np.hstack(tuple(arr))

def calculate_value(betas,x,degree):
    a = np.zeros(x.shape)
    for i in range(degree+1):
        a += betas[degree - i] * x ** i
    return a

def get_solution(degree,dt):
    print(f"degree {degree} -------------- \n")
    B=dt.values
    x,y = B[:,0],B[:,1]
    A = polynomial_matrix(x,degree)
    beta=np.dot(np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,y.T))
    print(beta)
    print("value on sample input")
    print(np.sum(beta * config.sample_input))

    plt.figure(figsize = (10,5))
    xl = np.linspace(min(x)-1,max(x)+1,num=100)
    plt.plot(xl,calculate_value(beta,xl,degree),c='r')
    plt.scatter(x,y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    plt.savefig(f'que2_{degree}.png')

    print("\n")


dt=pd.read_excel(config.xl_path)

get_solution(2,dt)
get_solution(3,dt)
get_solution(4,dt)
# get_solution(5,dt)
# get_solution(6,dt)
