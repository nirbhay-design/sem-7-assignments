import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

class Config:
    xl_path = sys.argv[1]
    sample_input_x = np.array([4000])
    sample_input_y = np.array([7])

config = Config()

def polynomial_matrix(x: np.array, y: np.array):
    arr = []
    arr.append((x**2).reshape(x.shape[0],1))
    arr.append((x*y).reshape(x.shape[0],1))
    arr.append((y**2).reshape(x.shape[0],1))
    arr.append((x).reshape(x.shape[0],1))
    arr.append((y).reshape(x.shape[0],1))
    arr.append(np.ones((x.shape[0],1)))
    return np.hstack(tuple(arr))

def get_solution(dt):
    B=dt.values
    x,y,z = B[:,0],B[:,1],B[:,2]
    A = polynomial_matrix(x,y)
    beta=np.dot(np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,z.T))
    print(beta)
    print("value on sample input")
    print(np.sum(beta * polynomial_matrix(config.sample_input_x, config.sample_input_y)))

dt=pd.read_excel(config.xl_path)

get_solution(dt)
