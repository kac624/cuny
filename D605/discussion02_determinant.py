#%%
import numpy as np
#%%

#%%
def determinant(matrix):
    if len(matrix) <= 1:
        return matrix[0, 0]

    else:
        products = []
        for i in range(len(matrix)):
            sign = (-1) ** (i + 2)
            element = matrix[0, i]
            submatrix = np.delete(np.delete(matrix, i, 1), 0, 0)
            sub_determ = determinant(submatrix)
            products.append(element * sub_determ * sign)

    return sum(products)
#%%

#%%
A = np.array([
    [1, 0, 1, 1],
    [2, 2,-1, 1],
    [2, 1, 3, 0],
    [1, 1, 0, 1]
])
#%%

#%%
np.linalg.det(A)
#%%

#%%
determinant(A)
#%%