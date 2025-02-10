import numpy as np

class CustomSVD :
    def __init__(self,A):
        self.__A=A

    def calc_svd(self):
        m, n = self.__A.shape
        eigen_values_U, eigen_vectors_U = np.linalg.eig(np.dot(self.__A, self.__A.T))  # gives U
        #(AAt)U=Sigma^2U
        # Sorting eigen_values_U and eigen_vectors_U in descending order of eigen_values_U
        idx = eigen_values_U.argsort()[::-1]
        eigen_values_U = eigen_values_U[idx]
        eigen_vectors_U = eigen_vectors_U[:, idx]
        eigen_values_U = np.real(eigen_values_U)
        eigen_vectors_U = np.real(eigen_vectors_U)
        # print("\n U ",eigen_vectors_U)
        eigen_values_V, eigen_vectors_V = np.linalg.eig(np.dot(self.__A.T, self.__A))  # gives V
        #(AtA)V=Sigma^2V
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
        # print(self.__A.shape)
        # print(eigen_vectors_U.shape)
        # print("\n")
        # print(Sigma.shape)
        # print("\n")
        # print(eigen_vectors_V.T.shape)
        # print("\n")
        # print(eigen_vectors_V.T.shape)
        return eigen_vectors_U, Sigma, eigen_vectors_V.T
