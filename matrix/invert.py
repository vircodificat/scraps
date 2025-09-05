import random

def invert_4x4(m):
    # Build augmented matrix [m | I]
    aug = [m[i][:] + [1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]

    for i in range(4):
        # --- Pivot: find the row with the largest |entry| in column i at/under i
        pivot_row = max(range(i, 4), key=lambda r: abs(aug[r][i]))
        # Swap it into place (handles zero on the diagonal)
        if pivot_row != i:
            aug[i], aug[pivot_row] = aug[pivot_row], aug[i]

        # --- Normalize pivot row so pivot becomes 1
        pivot = aug[i][i]
        inv_pivot = 1.0 / pivot
        for j in range(8):
            aug[i][j] *= inv_pivot

        # --- Eliminate this column in all other rows
        for r in range(4):
            if r == i:
                continue
            factor = aug[r][i]
            if factor != 0.0:
                for j in range(8):
                    aug[r][j] -= factor * aug[i][j]

    # Extract right half as the inverse
    return [row[4:] for row in aug]


def zeroes():
    return [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
    ]

def rand_4x4():
    A = zeroes()
    for i in range(4):
        for j in range(4):
            A[i][j] = random.gauss()
    return A

## Example
#A = [
#    [1.0, 2.0, 3.0, 4.0],
#    [0.0, 0.0, 4.0, 3.0],
#    [0.0, 6.0, 0.0, 1.0],
#    [2.0, 0.0, 0.0, 1.0]
#]

A = rand_4x4()
A_inv = invert_4x4(A)

def mult(A, B):
    C = zeroes()

    for i in range(4):
        for j in range(4):
            sum = 0.0
            for k in range(4):
                sum += A[i][k] * B[k][j]
            if abs(sum) < 0.000001:
                sum = 0.0
            C[i][j] = sum
    return C


for row in A:
    print(row)

print()

for row in A_inv:
    print(row)

print()

C = mult(A, A_inv)
for row in C:
    print(row)
