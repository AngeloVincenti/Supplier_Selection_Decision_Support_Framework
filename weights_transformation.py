import networkx as nx
import numpy as np

from typing import Sequence


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    return vector/np.sum(vector)

def roc_weights_from_ranks(ranks: Sequence[int]) -> np.ndarray:
    """
    Calcola il vettore dei pesi ROC (Rank Order Centroid) a partire
    da un vettore di rank per criterio.

    Parametri
    ----------
    ranks : Sequence[int]
        ranks[j] = posizione in classifica del criterio j.
        Esempio: [3, 1, 2] significa:
            - criterio 0 ha rank 3
            - criterio 1 ha rank 1
            - criterio 2 ha rank 2

    Ritorna
    -------
    np.ndarray
        vettore dei pesi ROC nello stesso ordine dei criteri in input.

    Note
    ----
    Formula ROC:
        w_j = (1/n) * sum_{k=r_j}^{n} (1/k)

    dove r_j è il rank del criterio j.
    """

    ranks = np.asarray(ranks, dtype=int)
    n = len(ranks)

    if n == 0:
        raise ValueError("Il vettore dei rank non può essere vuoto.")

    # Verifica che i rank siano una permutazione di 1..n
    expected = set(range(1, n + 1))
    if set(ranks.tolist()) != expected:
        raise ValueError(
            f"I rank devono essere una permutazione di 1..{n}. "
            f"Ricevuto: {ranks.tolist()}"
        )

    weights = np.zeros(n, dtype=float)

    for j, r_j in enumerate(ranks):
        weights[j] = (1.0 / n) * sum(1.0 / k for k in range(r_j, n + 1))

    weights = normalize_vector(weights)

    return weights


def transformation_roc_vector(W_best, roc_vector):

    weights  = np.abs(W_best).dot(np.reshape(roc_vector,(-1,1)))
    weights = normalize_vector(weights)

    return  weights

def transformation_centrality(abs_graph_reversed,nodes):

    centrality = nx.eigenvector_centrality(abs_graph_reversed, weight="weight")

    weights = [centrality[n] for n in nodes]

    weights = np.array(weights)

    weights = normalize_vector(weights)

    return weights


def find_principal_eigenvector(matrix:np.ndarray) -> np.ndarray:
    w, v = np.linalg.eig(matrix)

    idx = np.argsort(-np.abs(w))

    v = v[:, idx]

    principal = np.real_if_close(v[:, 0])
    return principal


def normalize_by_max_row_sum(A):

    row_sums = A.sum(axis=1)
    max_row_idx = np.argmax(row_sums)

    max_sum = row_sums[max_row_idx]

    A_norm = A / max_sum

    return A_norm

def transformation_importance_matrix(connotation_mat, w_best):

    w_best_norm = normalize_by_max_row_sum(w_best)
    eigenvector = find_principal_eigenvector(connotation_mat)
    eigenvector = normalize_vector(eigenvector)

    weights = w_best_norm.dot(np.reshape(eigenvector, (-1, 1)))

    weights = normalize_vector(weights)

    return weights
