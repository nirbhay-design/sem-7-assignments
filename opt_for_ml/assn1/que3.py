import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

class Config:
    xl_path = sys.argv[1]
    sample_input = np.array([4000,4+3,])

config = Config()

dt=pd.read_excel(config.xl_path)
B=dt.values
x,y = B[:,0],B[:,1]
x = x.reshape((x.shape[0],1))
y = y.reshape((y.shape[0],1))
z = B[:,2]
np_ones = np.ones((x.shape[0],1),dtype=float)
A = np.hstack((x,y,np_ones))
beta=np.dot(np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,z.T))
print(beta)
print("value on sample input ")
print(beta[0] * config.sample_input[0] + beta[1] * config.sample_input[1] + beta[2])