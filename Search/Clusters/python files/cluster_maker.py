import random
import operator

import similarity_centroid_helper

document_vector_matrix_file = open('../Files/document_vector_matrix.txt', 'r')
urls_file = open('../../crawler/Files/urls.txt', 'r')

urls_file_lines = urls_file.readlines()
urls = []

for line in urls_file_lines:
    if line[len(line)-2] == '{' or len(line) < 3:
        pass
    else:
        urls.append(line.strip('\n'))


document_vector_matrix_lines = document_vector_matrix_file.readlines()

document_vector_matrix = {}

print('constructing document_vector_matrix')

for line in document_vector_matrix_lines:
    document_url = line[:line.index(' ')]
    document_vector = line[line.index(' ')+1:len(line)-1]
    document_vector = document_vector.strip().strip('{').strip('}')
    document_vector_token = document_vector.split(', ')
    for token_value_pair in document_vector_token:
        token_value = token_value_pair.split(': ')
        token_value[0] = token_value[0].strip('\'')
        token_value[1] = float(token_value[1])
        if document_url not in document_vector_matrix:
            document_vector_matrix[document_url] = {token_value[0]: token_value[1]}
        else:
            document_vector_matrix[document_url][token_value[0]] = token_value[1]

k = 50
max_iterations = 25
pages = 499

k_centroid_vector_matrix = {}
document_centroid_similarity_matrix = {}
prev_document_s_centroid = {}
document_s_centroid = {}
centroid_s_document = {}
cluster_name = {}

irrelevant_characters = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '[', ']', '\\', ';', '\'', ',', '.', '/', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '{', '}', '|', ':', '\"', '<', '>', '?']

print('Initializing centroids')

random_indexes = []


def initial_centroid():
    global random_indexes
    i = 0
    while i < k:
        random_index = random.randint(0, pages)
        if random_index not in random_indexes:
            random_indexes.append(random_index)
        else:
            # print("repeated")
            continue
        if urls[random_index] not in document_vector_matrix:
            # print('the document was not crawled because of some error')
            continue
        k_centroid_vector_matrix[i] = document_vector_matrix[urls[random_index]]
        i = i + 1


initial_centroid()


def doc_centroid_similarity():
    global document_centroid_similarity_matrix
    document_centroid_similarity_matrix = {}
    for document in document_vector_matrix:
        for centroid in k_centroid_vector_matrix:
            s = similarity_centroid_helper.cosine_similarity(document_vector_matrix[document], k_centroid_vector_matrix[centroid])
            if document not in document_centroid_similarity_matrix:
                document_centroid_similarity_matrix[document] = []
            document_centroid_similarity_matrix[document].append(s)


# doc_centroid_similarity()
# for document in document_centroid_similarity_matrix:
#     print(document, document_centroid_similarity_matrix[document])


def copy_doc_to_centroid():
    for document in document_s_centroid:
        prev_document_s_centroid[document] = document_s_centroid[document]


def allocate_doc_to_centroid():
    global centroid_s_document
    centroid_s_document = {}
    for document in document_centroid_similarity_matrix:
        max_s = 0
        pos = 0
        j = 0
        for i in document_centroid_similarity_matrix[document]:
            if i > max_s:
                pos = j
                max_s = i
            j += 1
        if urls.index(document) in random_indexes:
            if random_indexes[pos] != urls.index(document):
                print('probably an error would occur. ignore if convergence iteration is not 0')
        document_s_centroid[document] = pos
        if pos not in centroid_s_document:
            centroid_s_document[pos] = {}
        centroid_s_document[pos][document] = document_vector_matrix[document]

# allocate_doc_to_centroid()

'''
for document in document_s_centroid:
    print(document, document_s_centroid[document])
for centroid in centroid_s_document:
    print(centroid)
    for document in centroid_s_document[centroid]:
        print(document)
'''


def recalculate_centroid():
    for cluster in centroid_s_document:
        k_centroid_vector_matrix[cluster] = similarity_centroid_helper.centroid(centroid_s_document[cluster])

# recalculate_centroid()


def check_document_s_centroid():
    flag = True
    for document in document_s_centroid:
        if document in prev_document_s_centroid:
            if prev_document_s_centroid[document] == document_s_centroid[document]:
                pass
            else:
                flag = False
                break
    return flag

initial_cluster_file = open('../Files/initial_clusters.txt', 'w')

converged = False
convergence_iteration = 0
while ~converged and convergence_iteration < max_iterations:
    print("\nConvergence_iteration", convergence_iteration)
    print('Calculating similarity')
    doc_centroid_similarity()
    print("Copying centroid allocated to documents")
    copy_doc_to_centroid()
    print('Assigning centroids')
    allocate_doc_to_centroid()
    print('Recalculating centroids')
    recalculate_centroid()
    print('Checking centroids')
    converged = check_document_s_centroid()
    convergence_iteration += 1
    if convergence_iteration == 1:
        for centroid in range(0, len(centroid_s_document)):
            initial_cluster_file.write(str(centroid) + " " + str(len(centroid_s_document[centroid])) + "\n")
            # print(centroid, len(centroid_s_document[centroid]))
            for document in centroid_s_document[centroid]:
                initial_cluster_file.write(str(document) + "\n")
                # print(document)

        for centroid_vector in k_centroid_vector_matrix:
            sorted_k_centroid_vector_matrix_i = sorted(k_centroid_vector_matrix[centroid_vector].items(),
                                                       key=operator.itemgetter(1), reverse=True)
            for i in range(0, len(sorted_k_centroid_vector_matrix_i)):
                irrelevant_flag = 0
                for character in irrelevant_characters:
                    if character in sorted_k_centroid_vector_matrix_i[i][0]:
                        irrelevant_flag = 1
                        break
                if irrelevant_flag == 0:
                    cluster_name[centroid_vector] = sorted_k_centroid_vector_matrix_i[i][0]
                    break

initial_cluster_file.close()

print("convergence_iteration", convergence_iteration)

for centroid_vector in k_centroid_vector_matrix:
    sorted_k_centroid_vector_matrix_i = sorted(k_centroid_vector_matrix[centroid_vector].items(), key=operator.itemgetter(1), reverse=True)
    for i in range(0, len(sorted_k_centroid_vector_matrix_i)):
        irrelevant_flag = 0
        for character in irrelevant_characters:
            if character in sorted_k_centroid_vector_matrix_i[i][0]:
                irrelevant_flag = 1
                break
        if irrelevant_flag == 0:
            cluster_name[centroid_vector] = sorted_k_centroid_vector_matrix_i[i][0]
            break

final_cluster_file = open('../Files/final_clusters.txt', 'w')

for centroid in range(0, len(centroid_s_document)):
    final_cluster_file.write("{" + str(centroid) + " " + str(len(centroid_s_document[centroid])) + " " + cluster_name[centroid] + "}" + "\n")
    # print(centroid, len(centroid_s_document[centroid]))
    for document in centroid_s_document[centroid]:
        final_cluster_file.write(str(document) + "\n")
        # print(document)

final_cluster_file.close()
