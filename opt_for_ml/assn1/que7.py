import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

class Config:
    xl_path = sys.argv[1]
    save_fig_path = sys.argv[2]

config = Config()

def calculate_value(x, beta0, beta1):
    return beta0 * np.exp(beta1 * x)


dt=pd.read_excel(config.xl_path)
B=dt.values
x,y=B[:,0],B[:,1]
y = np.log(y)
np_ones = np.ones((len(x),1),dtype=float)
A=np.column_stack((x,np_ones))
beta=np.dot(np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,y.T))
beta[1] = np.exp(beta[1])
print(beta)
plt.figure(figsize = (10,5))
plt.scatter(x, y,c='r')
plt.plot(x, calculate_value(x,beta[1],beta[0]))
plt.xlabel('x')
plt.ylabel('y')
plt.show()
plt.savefig(config.save_fig_path)

print(calculate_value(np.array([2021]),beta[1],beta[0]))
