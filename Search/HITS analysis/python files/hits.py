import numpy


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


def matrix_multiplication(matrix_a, matrix_b):
    product = numpy.dot(matrix_a, matrix_b)
    return product

print('Constructing adjacency matrix')

adjacency_mat_file = open('../../Crawler/Files/doc_adjacency_matrix.txt', 'r')

adjacency_mat_lines = adjacency_mat_file.readlines()

adjacency_mat = []

for line in adjacency_mat_lines:
    if line[0] != '[':
        pass
    else:
        line = line[1:len(line) - 2]
        values = line.split(', ')
        for j in range(0, len(values)):
            values[j] = int(values[j])
        adjacency_mat.append(values)

binary_adjacency_mat = [[0 for x in range(0, len(adjacency_mat[0]))] for y in range(0, len(adjacency_mat))]

print('Constructing binary adjacency matrix')

for i in range(0, len(adjacency_mat)):
    for j in range(0, len(adjacency_mat[0])):
        if adjacency_mat[i][j] != 0:
            binary_adjacency_mat[i][j] = 1

binary_adjacency_mat_transpose = matrix_transpose(binary_adjacency_mat)

hub_score = {}
authority_score = {}


def hits():
    print('Multiplying matrices')
    hub_product_matrix = matrix_multiplication(binary_adjacency_mat, binary_adjacency_mat_transpose)
    authority_product_matrix = matrix_multiplication(binary_adjacency_mat_transpose, binary_adjacency_mat)
    print('Calculating eigen values and vectors')
    hub_matrix_eigen_values = numpy.linalg.eigvals(hub_product_matrix)
    authority_matrix_eigen_values = numpy.linalg.eigvals(authority_product_matrix)
    hub_matrix_eigen_vector = numpy.linalg.eig(hub_product_matrix)
    hub_matrix_eigen_vector = hub_matrix_eigen_vector[1:][0]
    authority_matrix_eigen_vector = numpy.linalg.eig(authority_product_matrix)
    authority_matrix_eigen_vector = authority_matrix_eigen_vector[1:][0]

    print('Calculating hub score')

    hub_eig_val_count = 0

    for eigen_value_index in range(0, len(hub_matrix_eigen_values)):
        if numpy.absolute(numpy.absolute(hub_matrix_eigen_values[eigen_value_index]) - 1) < 0.0002:
            hub_eig_val_count += 1
            for value_index in range(0, len(hub_matrix_eigen_vector[eigen_value_index])):
                if value_index not in hub_score:
                    hub_score[value_index] = numpy.absolute(hub_matrix_eigen_vector[eigen_value_index][value_index])
                else:
                    hub_score[value_index] += numpy.absolute(hub_matrix_eigen_vector[eigen_value_index][value_index])

    for index in hub_score:
        hub_score[index] = hub_score[index]/hub_eig_val_count
    print(hub_score)

    print('Calculating authority score')

    authority_eig_val_count = 0

    for eigen_value_index in range(0, len(authority_matrix_eigen_values)):
        if numpy.absolute(numpy.absolute(authority_matrix_eigen_values[eigen_value_index]) - 1) < 0.0002:
            authority_eig_val_count += 1
            for value_index in range(0, len(authority_matrix_eigen_vector[eigen_value_index])):
                if value_index not in authority_score:
                    authority_score[value_index] = numpy.absolute(authority_matrix_eigen_vector[eigen_value_index][value_index])
                else:
                    authority_score[value_index] += numpy.absolute(authority_matrix_eigen_vector[eigen_value_index][value_index])

    for index in authority_score:
        authority_score[index] = authority_score[index] / authority_eig_val_count
    print(authority_score)

hits()

print('Writing to file')

hub_score_file = open('../Files/hub_score.txt', 'w')
hub_score_file.write('Hub scores\n')

for i in hub_score:
    hub_score_file.write(str(i) + " " + str(hub_score[i]) + "\n")

hub_score_file.close()

authority_score_file = open('../Files/authority_score.txt', 'w')
authority_score_file.write('Authority scores\n')

for i in authority_score:
    authority_score_file.write(str(i) + " " + str(authority_score[i]) + "\n")

authority_score_file.close()
