import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import cvxopt as cp

class Config:
    xl_path = sys.argv[1]
    sample_input = np.array([4000,4+3,1])
    rows = int(sys.argv[2])
    lambd = 0.1

def l2_reg(A:np.array, label:np.array, lambd:float)->np.array:
    total_features, num_features = A.shape
    beta=np.dot(np.linalg.inv(np.dot(A.T,A) + lambd * np.eye(num_features)),np.dot(A.T,label))
    return beta


def l_inf_reg(A:np.array, label:np.array, lambd:float) -> np.array:
    Q11 = np.dot(A.T,A)
    Q12 = np.zeros((A.shape[1],1))
    Q21 = np.zeros((1,A.shape[1]))
    Q22 = np.zeros((1,1))
    Q = np.vstack([np.hstack([Q11,Q12]), np.hstack([Q21,Q22])])
    AT_b = -np.dot(A.T,label)
    lambd_by_2 = np.array([[lambd/2] for _ in range(1)])
    c = np.vstack([AT_b,lambd_by_2])
    G11 = np.eye(A.shape[1])
    G12 = np.array([[-1] for _ in range(A.shape[1])])
    G21 = -np.eye(A.shape[1])
    G22 = np.array([[-1] for _ in range(A.shape[1])])
    G = np.vstack([np.hstack([G11,G12]), np.hstack([G21,G22])])
    h = np.zeros((A.shape[1]*2,1))
    sol = cp.solvers.qp(
        cp.matrix(Q,tc="d"), 
        cp.matrix(c,tc="d"),
        cp.matrix(G,tc="d"),
        cp.matrix(h,tc='d')
    )
    print(Q)
    print(c)
    print(G)
    print(h)
    print(Q.shape)
    print(c.shape)
    print(G.shape)
    print(h.shape)
    
    return np.array(sol['x'])

def l1_reg(A:np.array, label:np.array, lambd:float) -> np.array:
    Q11 = np.dot(A.T,A)
    Q12 = np.zeros_like(Q11)
    Q21 = np.zeros_like(Q11)
    Q22 = np.zeros_like(Q11)
    Q = np.vstack([np.hstack([Q11,Q12]), np.hstack([Q21,Q22])])
    AT_b = -np.dot(A.T,label)
    lambd_by_2 = np.array([[lambd/2] for _ in range(A.shape[1])])
    c = np.vstack([AT_b,lambd_by_2])
    G11 = np.eye(A.shape[1])
    G12 = -np.eye(A.shape[1])
    G21 = -np.eye(A.shape[1])
    G22 = -np.eye(A.shape[1])
    G = np.vstack([np.hstack([G11,G12]), np.hstack([G21,G22])])
    h = np.zeros((A.shape[1]*2,1))
    sol = cp.solvers.qp(
        cp.matrix(Q,tc="d"), 
        cp.matrix(c,tc="d"),
        cp.matrix(G,tc="d"),
        cp.matrix(h,tc='d')
    )
    return np.array(sol['x'])

if __name__ == "__main__":
    config = Config()
    dt=pd.read_excel(config.xl_path)
    B=dt.values
    features, label = B[:config.rows,0:-1],B[:config.rows,-1:]
    np_ones = np.ones((features.shape[0],1),dtype=float)
    A = np.hstack((features,np_ones))
    lambd = config.lambd
    wts_l2 = l2_reg(A,label, lambd)    
    wts_l1 = l1_reg(A,label,lambd)
    wts_li = l_inf_reg(A,label,lambd)
    print(wts_l2)
    print(wts_l1)
    print(wts_li)