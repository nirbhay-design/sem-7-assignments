import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import math

class Config:
    xl_path = sys.argv[1]

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

def calculate_loss(betas,x,y,degree):
    a = np.zeros(x.shape)
    for i in range(degree+1):
        a += betas[degree - i] * x ** i 
    shape = x.shape[0]   
    return np.sum((a-y) ** 2) / (2*shape)

def get_solution(degree,dt):
    print(f"degree {degree} -------------- \n")
    B=dt.values
    x,y = B[:,0],B[:,1]
    A = polynomial_matrix(x,degree)
    beta=np.dot(np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,y.T))

    plt.figure(figsize = (10,5))
    xl = np.linspace(min(x)-1,max(x)+1,num=100)
    plt.plot(xl,calculate_value(beta,xl,degree),c='r')
    plt.scatter(x,y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'degree: {degree}')
    plt.show()
    plt.savefig(f'que8_{degree}.png')

    return x, y, beta

dt=pd.read_excel(config.xl_path)


betas = [None]
all_avg_loss = [None]
min_avg_loss = math.inf
optimal_degree = -1
for i in range(1,21):
    x, y, beta = get_solution(i,dt)

    loss = calculate_loss(beta,x,y,i);

    if loss < min_avg_loss:
        min_avg_loss = loss;
        optimal_degree = i
    
    betas.append(beta)
    all_avg_loss.append(loss)


print(f"optimal_degree: {optimal_degree}")
print(f"avg loss at {optimal_degree} degree: {min_avg_loss:.2f}")

print(all_avg_loss)

print(betas[9])