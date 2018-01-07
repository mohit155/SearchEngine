import matrix_helper

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

binary_out_degree_row_count = {}


for i in range(0, len(adjacency_mat)):
    for j in range(0, len(adjacency_mat[0])):
        if adjacency_mat[i][j] != 0:
            binary_adjacency_mat[i][j] = 1
            if i not in binary_out_degree_row_count:
                binary_out_degree_row_count[i] = 1
            else:
                binary_out_degree_row_count[i] += 1

trans_inv_count_adjacency_mat = [[0 for xt in range(0, len(adjacency_mat))] for yt in range(0, len(adjacency_mat[0]))]

for i in range(0, len(binary_adjacency_mat)):
    for j in range(0, len(binary_adjacency_mat[0])):
        if i in binary_out_degree_row_count:
            trans_inv_count_adjacency_mat[j][i] = binary_adjacency_mat[i][j]/binary_out_degree_row_count[i]

dampling_factor = 0.85


def rank():
    dm = matrix_helper.scalar_multiplication(trans_inv_count_adjacency_mat, dampling_factor)
    identity_matrix = matrix_helper.identity_matrix(len(trans_inv_count_adjacency_mat), len(trans_inv_count_adjacency_mat[0]))
    i_dm = matrix_helper.subtract(identity_matrix, dm)
    inv_i_dm = matrix_helper.inverse_matrix(i_dm)
    unity_col_mat = matrix_helper.unitary_col_matrix(len(trans_inv_count_adjacency_mat))
    cold_start_factor = (1 - dampling_factor)/len(trans_inv_count_adjacency_mat)
    cold_start_matrix = matrix_helper.scalar_multiplication_unary(unity_col_mat, cold_start_factor)
    page_rank = matrix_helper.matrix_multiplication(inv_i_dm, cold_start_matrix)
    return page_rank

page_rank = rank()

page_rank_file = open('../Files/page_rank.txt', 'w')
page_rank_file.write("Page Rank\n")

for i in range(0, len(page_rank)):
    page_rank_file.write(str(i) + " " + str(page_rank[i]) + "\n")

page_rank_file.close()
