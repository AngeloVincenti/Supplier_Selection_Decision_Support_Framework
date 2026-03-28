
import numpy as np
from classes import Selector
from typing import Tuple



def sep():
    print("-----------------------------------------------------------------------------------------")




def extract_range(X):

    X = np.array(X)
    selectors = []
    for i in range(X.shape[0]):
        s = Selector([],[])
        for j in range(X.shape[1]) :
            s.vet_min.append(X[i][j].a)
            s.vet_max.append(X[i][j].c)
        selectors.append(s)

    for selector in selectors:
       normalize_min_max_vectors(selector)


    return selectors


def normalize_min_max_vectors(selector):


    min_vec = selector.vet_min
    max_vec = selector.vet_max


    min_vec = np.array(min_vec)
    max_vec = np.array(max_vec)

    global_min = np.min(min_vec)
    global_max = np.max(max_vec)



    if global_max == global_min:
        raise ValueError("Global max equals global min.")

    min_norm = (min_vec - global_min) / (global_max - global_min)
    max_norm = (max_vec - global_min) / (global_max - global_min)

    selector.set_bounds(min_norm,max_norm)



def flatten_weights(W: np.ndarray, mask: np.ndarray) -> np.ndarray:
    return W[mask]


def unflatten_weights(vec: np.ndarray, template_shape: Tuple[int, int], mask: np.ndarray) -> np.ndarray:
    W = np.zeros(template_shape, dtype=float)
    W[mask] = vec
    np.fill_diagonal(W, 0.0)
    return W

def sigmoid(W: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-W))

def fcm_reasoning(A0: np.ndarray, W: np.ndarray, steps: int = 10) -> np.ndarray:
    A = A0.astype(float).copy()

    for _ in range(steps):
        A = sigmoid(A + A @ W)
    return A

def fcm_reasoning_show(A0: np.ndarray, W: np.ndarray, steps: int = 10) -> np.ndarray:
    A = A0.astype(float).copy()

    for _ in range(steps):

        print(f"A{_}:{np.around(A, decimals=3)}")
        A = sigmoid(A + A @ W)
    return A

def constriction_factor(k:int ,c1: float, c2: float) -> float:
    phi = c1 + c2
    if phi <= 4.0:
        raise ValueError("phi = c1 + c2 must be > 4 for constriction formula")
    chi = 2.0*k / abs(2.0 - phi - np.sqrt(phi ** 2 - 4.0 * phi))
    return chi



def pso(
    w_init: np.ndarray,
    A0,
    selector_list: list[Selector] = None,
    swarm_size: int = 30,
    iterations: int = 200,
    c1: float = 2.05,
    c2: float = 2.05,
    seed: int = 0,
) -> Tuple[np.ndarray, float]:


    rng = np.random.default_rng(seed)

    mask = np.array(w_init != 0)


    dim = int(mask.sum())


    lb_mat = -1 * np.ones_like(w_init)
    ub_mat = 1 * np.ones_like(w_init)
    lb = flatten_weights(lb_mat, mask)
    ub = flatten_weights(ub_mat, mask)


    w0_flat = flatten_weights(w_init, mask)


    pos = np.array([rng.uniform(lb, ub) for _ in range(swarm_size)])


    pos = (pos + w0_flat) / 2.0

    vel = np.zeros_like(pos)

    chi = constriction_factor(1, c1, c2)

    pbest_pos = pos.copy()
    pbest_val = np.full(swarm_size, np.inf)


    for i in range(swarm_size):
        W_i = unflatten_weights(pos[i], w_init.shape, mask)
        val = fitness_heaviside(W_i,A0,selectors=selector_list)
        if val < pbest_val[i]:
          pbest_val[i] = val

    gbest_idx = int(np.argmin(pbest_val))
    gbest_pos = pbest_pos[gbest_idx].copy()
    gbest_val = pbest_val[gbest_idx]
    print(gbest_val)


    # PSO main loop
    for t in range(iterations):
        r1 = rng.random((swarm_size, dim))
        r2 = rng.random((swarm_size, dim))

        cognitive = c1 * r1 * (pbest_pos - pos)
        social = c2 * r2 * (gbest_pos - pos)

        vel = chi * (vel + cognitive + social)

        pos = pos + vel

        pos = np.minimum(pos, ub)
        pos = np.maximum(pos, lb)

        # evaluate
        for i in range(swarm_size):
            W_i = unflatten_weights(pos[i], w_init.shape, mask)
            val = fitness_heaviside(W_i,A0,selectors=selector_list)
            if val < pbest_val[i]:
                pbest_val[i] = val
                pbest_pos[i] = pos[i].copy()
                if val < gbest_val:
                    gbest_val = val
                    print(gbest_val)
                    gbest_pos = pos[i].copy()



    best_W = unflatten_weights(gbest_pos, w_init.shape, mask)
    return best_W, gbest_val


def fitness_heaviside(W_mat: np.ndarray,
                      A0: np.ndarray,
                      steps: int = 30,
                      selectors: list[Selector] = None,
                     ):

    Aout = fcm_reasoning(A0, W_mat, steps=steps)

    H = lambda x: (x >= 0).astype(float)
    fitness_total = 0

    for s in range(len(selectors)):
         term_low = H(selectors[s].vet_min - Aout) * np.abs(selectors[s].vet_min - Aout)
         term_high = H(Aout - selectors[s].vet_max) * np.abs(selectors[s].vet_max - Aout)

         sum_low = float(np.sum(term_low))
         sum_high = float(np.sum(term_high))

         fitness_total = sum_low + sum_high


    return fitness_total




def print_matrix(M, decimals=3):
    M = np.asarray(M)
    n_rows, n_cols = M.shape

    # Formatter for values
    def fmt(x):
        return f"{x:.{decimals}f}"

    # Matrix formatted as strings
    S = [[fmt(M[i, j]) for j in range(n_cols)] for i in range(n_rows)]

    # Compute column widths
    widths = [
        max(len(S[i][j]) for i in range(n_rows))
        for j in range(n_cols)
    ]

    # Column header
    header = "     " + " ".join(
        f"C{j+1}".rjust(widths[j]) for j in range(n_cols)
    )
    print(header)

    # Separator
    print("     " + "-" * (sum(widths) + n_cols - 1))

    # Print rows with labels
    for i in range(n_rows):
        row = " ".join(
            S[i][j].rjust(widths[j]) for j in range(n_cols)
        )
        print(f"C{i+1}| {row}")




