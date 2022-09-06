import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

class Config:
    xl_path = sys.argv[1]
    sample_input = np.array([4000,4+3,1])

config = Config()

dt=pd.read_excel(config.xl_path)
B=dt.values
features, label = B[:,0:-1],B[:,-1]
np_ones = np.ones((features.shape[0],1),dtype=float)
A = np.hstack((features,np_ones))
beta=np.dot(np.linalg.inv(np.dot(A.T,A)),np.dot(A.T,label.T))
print(beta)
w_t = beta[:-1]
b = beta[-1]
print("value on sample input ")
print(np.sum(w_t * config.sample_input) + b)