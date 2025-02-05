import numpy as np


def calc_svd(A):
    m, n = A.shape
    eigen_values_U, eigen_vectors_U = np.linalg.eig(np.dot(A, A.T))  # gives U
    # Sorting eigen_values_U and eigen_vectors_U in descending order of eigen_values_U
    idx = eigen_values_U.argsort()[::-1]
    eigen_values_U = eigen_values_U[idx]
    eigen_vectors_U = eigen_vectors_U[:, idx]
    eigen_values_U = np.real(eigen_values_U)
    eigen_vectors_U = np.real(eigen_vectors_U)
    # print("\n U ",eigen_vectors_U)
    eigen_values_V, eigen_vectors_V = np.linalg.eig(np.dot(A.T, A))  # gives V
    # Sorting eigen_values_V and eigen_vectors_V in descending order of eigen_values_V
    eigen_values_V = np.real(eigen_values_V)
    eigen_vectors_V = np.real(eigen_vectors_V)
    idx = eigen_values_V.argsort()[::-1]
    eigen_values_V = eigen_values_V[idx]
    eigen_vectors_V = eigen_vectors_V[:, idx]
    # print("\n Vt \n",eigen_vectors_V.T)
    singular_values = np.sqrt(np.real(eigen_values_V[: min(m, n)]))
    # print("\n singular_values",singular_values)
    Sigma = np.zeros((m, n))
    np.fill_diagonal(Sigma, singular_values)
    # print(" \n Sigma \n",Sigma)
    # u, s, vt = np.linalg.svd(A)
    # print(vt)
    return eigen_vectors_U, Sigma, eigen_vectors_V.T
