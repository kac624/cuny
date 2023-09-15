#%%
import numpy as np
import sympy as sym
#%%

#%%
A = np.array([
    [-7, -1, 11, 0, -4],
    [4, 1, 0, 2, 0],
    [-10, -1, 14, 0, -4],
    [8, 2, -15, -1, 5],
    [-10, -1, 16, 0, -6]
])

x_vector = np.array([0,8,2,1,2])

print(A, '\n\n', x_vector)
#%%

#%%
S = np.array([
    x_vector,
    A@x_vector,
    A@A@x_vector,
    A@A@A@x_vector,
    A@A@A@A@x_vector,
    A@A@A@A@A@x_vector
]).T

print(S)
#%%

#%%
S_rref = sym.Matrix(S).rref()[0]
S_rref
#%%
x_values = [1, 1, 1, 1, 0, 0]
S_rref_solve = S_rref.copy()

for i in range(len(x_values)):
    S_rref_solve.col_del(i)
    S_rref_solve = S_rref_solve.col_insert(i, S_rref[:, [i]] * x_values[i])

x_1 = -sum(S_rref_solve[[0], [3, 4, 5]])
x_2 = -sum(S_rref_solve[[1], [3, 4, 5]])
x_3 = -sum(S_rref_solve[[2], [3, 4, 5]])

print(
    f'x_1 = {x_1}'
    f'\nx_2 = {x_2}'
    f'\nx_3 = {x_3}'
    f'\nx_4 = 1'
)
#%%

#%%
x = sym.symbols('x')
expression = x**3 - 3*x**2 - x + 3
roots = sym.solve(expression, x, cubics = False)
roots
#%%

#%%
final_results = {}

for i in range(len(roots)):

    roots = roots[-1:] + roots[:-1]

    k = 0
    factors = np.identity(len(A))
    result = []

    for root in roots:
        k += 1
        factor = (A - root * np.identity(len(A))).astype(float)
        factors = factor @ factors
        result.append(factors @ x_vector)
        if all(factors @ x_vector == 0):
            break

    eigenvector = result[-2]
    eigenvalue = roots[k - 1]

    final_results[eigenvalue] = eigenvector

final_results
#%%

#%%
print(
    f'Eigenvector (x) for λ = 3: {final_results[3]}\n'
    f'A @ x: {A @ final_results[3]}\n'
    f'λ @ x: {3 * final_results[3]}\n'
    f'Product of A @ x divided by x: {(A @ final_results[3]) / final_results[3]}'
)
#%%

#%%
random_vector = np.random.randint(1,10,5)

print(
    f'Random vector (x): {random_vector}\n'
    f'A @ x: {A @ random_vector}\n'
    f'λ @ x: {3 * random_vector}\n'
    f'Product of A @ x divided by x: {(A @ random_vector) / random_vector}'
)
#%%

#%%
vals, vecs = np.linalg.eig(A)

print(
    f'Eigenvalue (λ): {round(vals[0])}\n'
    f'Eigenvector (x): {vecs[:,0]}\n'
    f'A @ x: {A @ vecs[:,0]}\n'
    f'λ * x: {vals[0] * vecs[:,0]}\n'
    f'Product of A @ x divided by x: {(A @ vecs[:,0]) / vecs[:,0]}'
)
#%%


