token_document_ii_file = open('../../crawler/Files/token_document_ii.txt', 'r')
urls_file = open('../../crawler/Files/urls.txt', 'r')

urls_file_lines = urls_file.readlines()
urls = []

document_vector_matrix = {}

for line in urls_file_lines:
    if line[len(line)-2] == '{' or len(line) < 3:
        pass
    else:
        urls.append(line.strip('\n'))

token_document_ii_file_lines = token_document_ii_file.readlines()

for line in token_document_ii_file_lines:
    if line[len(line)-2] == '{' or len(line) < 3:
        pass
    else:
        token = line[:line.index(' ')]
        doc_freq_list = line[line.index(' ')+2:len(line)-2]
        doc_freq_list_values = doc_freq_list.split('}, {')
        for value in doc_freq_list_values:
            value = value.strip().strip('{')
            value_keys = value.split(', ')
            if len(value_keys) == 2:
                value_left_keys_value = value_keys[0].split(': ')
                value_right_keys_value = value_keys[1].split(': ')
                if urls[int(value_left_keys_value[0])-1] not in document_vector_matrix:
                    document_vector_matrix[urls[int(value_left_keys_value[0])-1]] = {token: float(value_right_keys_value[1])}
                else:
                    document_vector_matrix[urls[int(value_left_keys_value[0])-1]][token] = float(value_right_keys_value[1])

document_vector_matrix_file = open('../Files/document_vector_matrix.txt', 'w')

for i in document_vector_matrix:
    document_vector_matrix_file.write(i + " " + str(document_vector_matrix[i]) + "\n")

document_vector_matrix_file.close()
