import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

class Config:
    xl_path = sys.argv[1]
    save_fig_path = sys.argv[2]
    sample_input = np.array([4000,])

config = Config()

dt=pd.read_excel(config.xl_path)
B=dt.values
x,y=B[:,0],B[:,1]
np_ones = np.ones((len(x),1),dtype=float)
A=np.column_stack((x,np_ones))
beta=np.dot(np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,y.T))
print(beta)
plt.figure(figsize = (10,5))
plt.scatter(x, y,c='r')
plt.plot(x, beta[0]*x+beta[1])
plt.xlabel('x')
plt.ylabel('y')
plt.show()
plt.savefig(config.save_fig_path)

print("value on sample input ")
print(beta[0] * config.sample_input + beta[1])