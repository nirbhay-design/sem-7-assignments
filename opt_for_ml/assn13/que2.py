import numpy as np
import warnings
warnings.filterwarnings("ignore")

def calculate_f(x:np.array):
    """
    x: shape(N,1)
    """

    f_val = x[0] ** 2 + x[1] ** 2 + 2 * (x[2] ** 2) + x[3] ** 2 - 5 * x[0] - 5 * x[1] - 21 * x[2] + 7 * x[3]
    return f_val[0]

def calculate_g1(x:np.array):
    """
    x: shape(N,1)
    """

    g1_value = x[0] ** 2 + x[1] ** 2 + x[2] ** 2 + x[3] ** 2 + x[0] - x[1] + x[2] - x[3] - 8
    return g1_value[0]

def calculate_g2(x:np.array):
    """
    x: shape(N,1)
    """

    g2_value = x[0] ** 2 + 2 * (x[1] ** 2) + x[2] ** 2 + 2 * (x[3] ** 2) - x[0] - x[3] - 10
    return g2_value[0]

def cal_f(x_t:np.array, sigma):
    """
    x_t: shape(N+1,1) ([...t])
    """
    t = x_t[-1][0]
    g1 = calculate_g1(x_t[:-1,:])
    g2 = calculate_g2(x_t[:-1,:])
    log_barrier = (np.log(t-g1) + np.log(t-g2)) / sigma
    return t - log_barrier

def grad_f(x:np.array, sigma):
    """
    x: shape(N+1,1)
    """

    h = 1e-5
    grad_vector = []
    cur_f = cal_f(x, sigma)
    for i in range(x.shape[0]):
        x[i] += h
        new_f = cal_f(x, sigma)
        x[i] -= h
        grad = (new_f - cur_f) / h
        grad_vector.append(grad)
    return np.array(grad_vector,dtype=np.float64).reshape(-1,1)

def check_armijo_wolf_cond(x_k: np.array, d_k: np.array, alpha:float, beta1:float, beta2:float, sigma:int) -> bool:
    xk_alp_dk = x_k + alpha * d_k;
    f_grad = grad_f(x_k, sigma);
    f_grad_alph = grad_f(xk_alp_dk, sigma)
    armijo_left = cal_f(xk_alp_dk, sigma);
    armijo_right = cal_f(x_k, sigma) + alpha * beta1 *np.dot(f_grad.T,d_k);

    wolf_left = np.dot(f_grad_alph.T, d_k)
    wolf_right = beta2 * np.dot(f_grad.T,d_k);

    return (armijo_left <= armijo_right) and (wolf_left >= wolf_right) 


def steepest_direction(x_k:np.array, d_k:np.array, beta1: float, beta2: float, r:float, sigma:int) -> float:
    alpha = 1;
    while not check_armijo_wolf_cond(x_k, d_k, alpha, beta1, beta2, sigma):
        alpha = alpha * r
    return alpha;

def update_b(B:np.array, x_k_1:np.array, x_k:np.array, sigma:int) -> np.array:
    del_k = x_k - x_k_1;
    s_k = grad_f(x_k, sigma) - grad_f(x_k_1, sigma)
    first_term = s_k @ s_k.T
    second_term = del_k.T @ s_k
    third_term = B @ s_k @ s_k.T @ B
    fourth_term = s_k.T @ B @ s_k
    return B + (first_term/second_term) - (third_term/fourth_term) 

def find_x(x_0:np.array, B:np.array, beta1:float, beta2:float, sigma:int, epsilon:float, r:float) -> np.array:
    x_k = x_0
    d_k = -np.dot(np.linalg.inv(B),grad_f(x_k, sigma))
    norm_grad = np.linalg.norm(-d_k)

    iterations = 0
    while norm_grad > epsilon:
        alpha = steepest_direction(x_k, d_k, beta1, beta2, r, sigma);
        x_k_1 = x_k
        x_k = x_k + alpha * d_k
        B = update_b(B, x_k_1, x_k, sigma)
        d_k = -np.dot(np.linalg.inv(B),grad_f(x_k,sigma))
        norm_grad = np.linalg.norm(-d_k)
        iterations += 1
        if iterations == 1000:
            break;
    return x_k, iterations

x = np.zeros((4,1))
t = max(calculate_g1(x), calculate_g2(x)) + 1
x_t = np.vstack([x,np.array([[t]],dtype=np.float64)])
sigma = 10
beta1 = 1e-4;
beta2 = 0.9;
epsilon = 0.001
r = 0.5
B = np.eye(x_t.shape[0],dtype=np.float64)

print(find_x(x_t, B, beta1, beta2, sigma, epsilon, r))