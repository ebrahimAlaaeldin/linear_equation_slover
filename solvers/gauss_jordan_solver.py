from mpmath import mp, matrix
from solvers.solver import Solver

class GaussJordanSolver(Solver):
    
    def solve(self):
        augmented_matrix = self.gauss_jordan_elimination()
        solution = self.back_substitution(augmented_matrix)
        return solution

    def gauss_jordan_elimination(self):
        A,B = self.A, self.B
        augmented_matrix = matrix([[A[i, j] for j in range(A.cols)] + [B[i, 0]] for i in range(A.rows)])
        n = augmented_matrix.rows

        self.steps.append("Initial Augmented Matrix:")
        self.steps.append(augmented_matrix.copy())

        for i in range(n):
            max_index = max(range(i, n), key=lambda x: abs(augmented_matrix[x, i]))

            if i != max_index:
                self.steps.append(f"\nSwapping rows {i + 1} and {max_index + 1}:")
                augmented_matrix[i, :], augmented_matrix[max_index, :] = augmented_matrix[max_index, :], augmented_matrix[i, :]
                self.steps.append(augmented_matrix.copy())

            if augmented_matrix[i,i] != 1:
                pivot = augmented_matrix[i, i]
                augmented_matrix[i, :] /= pivot
                self.steps.append(f"\nRow {i + 1} /= {pivot}:")
                self.steps.append(augmented_matrix.copy())

            for j in range(n):
                if i != j:
                    if augmented_matrix[j,i]!=0:
                        multiplier = augmented_matrix[j, i]
                        augmented_matrix[j, :] -= multiplier * augmented_matrix[i, :]
                        self.steps.append(f"\nRow {j + 1} -= {multiplier} * Row {i + 1}:")
                        self.steps.append(augmented_matrix.copy())

        return augmented_matrix

    def back_substitution(self, augmented_matrix):
        n = augmented_matrix.rows
        solution = matrix([mp.mpf(0)] * n)  

        for i in range(n - 1, -1, -1):
            solution[i] = mp.mpf(augmented_matrix[i, n]) 

            for j in range(i + 1, n):
                solution[i] -= mp.mpf(augmented_matrix[i, j]) * solution[j]

            solution[i] /= mp.mpf(augmented_matrix[i, i])

        return solution


# Example
# A = matrix([[-8, 1, -2],
#             [-3, -1, 7],
#             [2, -6, 1]])

# B = matrix([[106.8],
#             [177.2],
#             [279.2]])


# a = GaussJordanSolver()
# solution = a.back_substitution(a.gauss_jordan_elimination(A,B))
# self.steps.append("\nSolution:")
# self.steps.append(solution)
