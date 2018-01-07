import numpy

scalar_number = 0.85
mat_a = [
    [1, 2],
    [2, 3],
    [3, 4],
]

mat_b = [
    [1, 2],
    [2, 3],
    [3, 4],
]

mat_c = [
    [1, 2, 3],
    [2, 3, 4],
    [3, 4, 5],
]


def subtract(minuend, subtrahend):
    row_minuend = len(minuend)
    col_minuend = 0
    if row_minuend > 0:
        col_minuend = len(minuend[0])
    row_subtrahend = len(subtrahend)
    col_subtrahend = 0
    if row_subtrahend > 0:
        col_subtrahend = len(subtrahend[0])
    # print("[", row_minuend, "*", col_minuend, "]", " ", "[", row_subtrahend, "*", col_subtrahend, "]")
    if row_minuend == row_subtrahend and col_minuend == col_subtrahend:
        result = [[0 for x in range(0, col_minuend)] for y in range(0, row_minuend)]
        for i in range(0, row_minuend):
            for j in range(0, col_minuend):
                result[i][j] = minuend[i][j] - subtrahend[i][j]
        return result


def scalar_multiplication(matrix, scalar):
    row_matrix = len(matrix)
    col_matrix = 0
    if row_matrix > 0:
        col_matrix = len(matrix[0])
    result = [[0 for x in range(0, col_matrix)] for y in range(0, row_matrix)]
    for i in range(0, row_matrix):
        for j in range(0, col_matrix):
            result[i][j] = scalar*matrix[i][j]
    return result


def scalar_multiplication_unary(matrix, scalar):
    row_matrix = len(matrix)
    result = [0 for y in range(0, row_matrix)]
    for i in range(0, row_matrix):
        result[i] = scalar*matrix[i]
    return result


def identity_matrix(row, col):
    matrix = [[0 for x in range(0, col)] for y in range(0, row)]
    for i in range(0, row):
        for j in range(0, col):
            if i == j:
                matrix[i][j] = 1

    return matrix


def inverse_matrix(matrix):
    inv_mat = numpy.linalg.inv(matrix)
    return inv_mat


def matrix_multiplication(matrix_a, matrix_b):
    product = numpy.dot(matrix_a, matrix_b)
    return product


def unitary_col_matrix(row):
    mat = [1 for x in range(0, row)]
    return mat


def matrix_transpose(matrix):
    row_matrix = len(matrix)
    col_matrix = 0
    if row_matrix > 0:
        col_matrix = len(matrix[0])
    transpose = [[0 for x in range(0, row_matrix)] for y in range(0, col_matrix)]
    for i in range(0, row_matrix):
        for j in range(0, col_matrix):
            transpose[j][i] = matrix[i][j]

    return transpose

