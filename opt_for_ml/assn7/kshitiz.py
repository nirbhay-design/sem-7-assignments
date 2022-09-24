from numpy import *

# def fun(x):
    
#     n  = len(x)
#     g = 1 + 9/(n-1)*sum([x[i] for i in range(1, n)])
#     h = 1 - pow(x[0]/g, 2)
#     res = h * g    
#     return res

def fun(x):
    return 4*x[0]**2 - 3* x[0]* x[1] + 2 * x[1]**2 - x[0] + 2*x[1]
    
def gradf(x):
    
    f0, n, h1 = fun(x), len(x), pow(10, -5)
    g = zeros((n, 1), dtype = float)
    
    for i in range(0, n):
        
        x1 = x.copy()
        x1[i] += h1
        # print(x, x1)
        g[i] = (fun(x1) - f0)/ h1
        
    return g

# ( R , R+1)
x0, beta1, beta2, r, eps, iter1 = array ([[14.0], [15.0]]), pow(10, -4), 0.9, 0.5, pow(10, -3), 0

print("Gradf(x0)", gradf(x0))

while linalg.norm(gradf(x0)) > eps:
    d0, alpha = -gradf(x0), 1
    # print("d0=", d0)
    while (fun(x0 + alpha * d0) > fun(x0) + alpha * beta1 * dot(gradf(x0).T, d0) or\
    dot(gradf(x0 + alpha*d0).T, d0)< beta2*dot(gradf(x0).T, d0)):
        alpha  = alpha * r
    
    # print(fun(x0+alpha*d0)-fun(x0))
    print(alpha)
    x0, iter1 = x0 + alpha * d0, iter1+1
    
print(x0, iter1)
        
    

