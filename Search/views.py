from django.shortcuts import render

from .forms import SearchForm

import math
import operator
import numpy


def index_search(request):
    x = 0
    post_get = 0
    context = {
        'x': x,
    }

    page = 1
    rel_fed = 0
    query = ''
    p_rel_fed = 0
    sorting = 'naive'
    hits = 0

    if 'search_query_get' in request.GET:
        query_g = request.GET['search_query_get']
        query = query_g
        post_get = 1
    if 'page' in request.GET:
        page = int(request.GET['page'])
    if 'rel_fed' in request.GET:
        rel_fed = int(request.GET['rel_fed'])
    if 'p_rel_fed' in request.GET:
        p_rel_fed = int(request.GET['p_rel_fed'])
    if 'sorting' in request.GET:
        sorting = request.GET['sorting']
    if 'hits' in request.GET:
        hits = int(request.GET['hits'])

    context['page'] = page
    context['rel_fed'] = rel_fed
    context['p_rel_fed'] = p_rel_fed
    context['sorting'] = sorting
    context['hits'] = hits

    if request.method == 'POST' or post_get == 1:
        if post_get == 0:
            query = request.POST['search_query']

        query_words = query.split(' ')
        d_id = {}
        page_rank_d_id = {}

        suggestion_string = ""
        if query != "":
            suggestion_string = bigram_spell_checker(query_words)

        for query_word in query_words:
            token_f = ""
            for token in token_document_ii:
                if query_word.lower() == token.lower():
                    token_f = token
                    break
            if token_f is not "":
                for token_i in token_document_ii[token_f]:
                    keys_value = list(token_i.keys())
                    if keys_value[0] not in d_id:
                        d_id[keys_value[0]] = token_i['TFID']
                    else:
                        d_id[keys_value[0]] += token_i['TFID']

                    if keys_value[0] not in page_rank_d_id:
                        if urls[int(keys_value[0])] in page_rank:
                            page_rank_d_id[keys_value[0]] = page_rank[urls[int(keys_value[0])-1]] * token_i['TFID']
                    else:
                        if urls[int(keys_value[0])] in page_rank:
                            page_rank_d_id[keys_value[0]] += page_rank[urls[int(keys_value[0])-1]] * token_i['TFID']

        sorted_d_id = sorted(d_id.items(), key=operator.itemgetter(1), reverse=True)
        sorted_page_rank_d_id = sorted(page_rank_d_id.items(), key=operator.itemgetter(1), reverse=True)

        documents = []
        document_titles = []

        documents_page_rank = []
        document_titles_page_rank = []

        j = 0
        for i_element in sorted_d_id:
            documents.append(urls[int(i_element[0]) - 1])
            document_titles.append(titles[urls[int(i_element[0]) - 1]])
            j += 1

        doc_hub_score = {}
        doc_authority_score = {}

        if hits == 1:
            doc_hub_score, doc_authority_score = hits_score(documents, sorted_d_id)

        j = 0
        for i_element in sorted_page_rank_d_id:
            documents_page_rank.append(urls[int(i_element[0]) - 1])
            document_titles_page_rank.append(titles[urls[int(i_element[0]) - 1]])
            j += 1

        recommended_cluster = {}
        recommended_cluster_name = ""

        if len(documents) > 0:
            for cluster in clusters:
                for cluster_url_title_pair in clusters[cluster]:
                    if documents[0] in cluster_url_title_pair:
                        recommended_cluster[cluster] = clusters[cluster]
                        recommended_cluster_name = cluster_names[cluster]
                        break
                if recommended_cluster_name != "":
                    break

        # context['documents'] = documents
        # context['document_titles'] = document_titles
        if sorting == 'page_rank':
            context['documents_titles'] = list(zip(documents_page_rank, document_titles_page_rank))
        else:
            context['documents_titles'] = list(zip(documents, document_titles))
        context['x'] = 1
        context['query'] = query
        context['suggestion_string'] = suggestion_string
        context['pager_length'] = range(1, int(math.ceil(len(documents)/10))+1)
        context['no_of_pages'] = int(math.ceil(len(documents) / 10))
        context['page'] = page
        context['list_range'] = "%d:%d" % ((page-1)*10, page*10)
        context['rel_fed'] = rel_fed
        context['p_rel_fed'] = p_rel_fed
        context['recommended_cluster'] = recommended_cluster
        context['recommended_cluster_name'] = recommended_cluster_name
        context['page_rank'] = page_rank
        """
        context['hub_score'] = hub_score
        context['authority_score'] = authority_score
        """
        context['doc_hub_score'] = doc_hub_score
        context['doc_authority_score'] = doc_authority_score
        context['sorting'] = sorting

        if rel_fed == 2 or p_rel_fed == 1:
            rel_fed_relevant_documents = []
            rel_fed_irrelevant_documents = []

            rel_fed_relevant_words = {}
            rel_fed_irrelevant_words = {}

            if rel_fed == 2:
                for document in documents:
                    if 'rel_fed_form_' + str(document) in request.POST:
                        if request.POST['rel_fed_form_'+str(document)] == '1':
                            rel_fed_relevant_documents.append(document)
                        else:
                            rel_fed_irrelevant_documents.append(document)
            if p_rel_fed == 1:
                for document in documents[:2]:
                    rel_fed_relevant_documents.append(document)

            for token in token_document_ii:
                for document in rel_fed_relevant_documents:
                    for doc_details in token_document_ii[token]:
                        if str((urls.index(document)+1)) in list(doc_details.keys()):
                            if token not in rel_fed_relevant_words:
                                rel_fed_relevant_words[token] = doc_details['TFID']
                            else:
                                rel_fed_relevant_words[token] += doc_details['TFID']
                for document in rel_fed_irrelevant_documents:
                    for doc_details in token_document_ii[token]:
                        if str((urls.index(document)+1)) in list(doc_details.keys()):
                            if token not in rel_fed_irrelevant_words:
                                rel_fed_irrelevant_words[token] = doc_details['TFID']
                            else:
                                rel_fed_irrelevant_words[token] += doc_details['TFID']
            rel_fed_relevant_words_sorted = sorted(rel_fed_relevant_words.items(), key=operator.itemgetter(1), reverse=True)

            rel_fed_irrelevant_words_sorted = sorted(rel_fed_irrelevant_words.items(), key=operator.itemgetter(1), reverse=True)

            count = 0

            rel_fed_suggestion_string = ""

            for query_word in query_words:
                if query_word in rel_fed_irrelevant_words_sorted[:5]:
                    pass
                else:
                    rel_fed_suggestion_string += query_word + " "

            for word in rel_fed_relevant_words_sorted:
                flag = 0
                for word1 in rel_fed_irrelevant_words_sorted[:5]:
                    if word[0] == word1[0]:
                        flag = 1
                        break
                if flag == 1:
                    pass
                else:
                    rel_fed_suggestion_string += word[0] + " "
                    count += 1
                if count == 5:
                    break

            context['rel_fed_suggestion_string'] = rel_fed_suggestion_string.strip()

        return render(request, 'Search/search.html', context)

    else:
        form = SearchForm()
        context['form'] = form
        return render(request, 'Search/search.html', context)


def index_cluster(request):
    context = {
        'clusters': clusters,
        'cluster_names': cluster_names,
    }
    return render(request, 'Search/clusters.html', context)

irrelevant_characters = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '[', ']', '\\', ';', '\'', ',', '.', '/', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '{', '}', '|', ':', '\"', '<', '>', '?']


def levenshtein_distance(word_a, word_b):
    count = 0
    word_b_characters = list(word_b)
    for character in word_a:
        if character in word_b_characters:
            word_b_characters.pop(word_b_characters.index(character))
        else:
            count += 1

    return len(word_b_characters) + count


def bigram_spell_checker(query_words):
    suggestion_word_list = {}
    suggestion_string = ""
    for query_word in query_words:
        flag = 0
        suggestion_word_list_q = {}
        for token in token_document_ii:
            if query_word.lower() == token.lower():
                flag = 1
                suggestion_word_list[query_word] = query_word
                suggestion_string += query_word + " "
                break
        if flag == 0:
            for char_i in range(len(query_word)-1):
                query_word_lower = query_word.lower()
                if (query_word_lower[char_i]+query_word_lower[char_i+1]) in bigrams:
                    for token_b in bigrams[query_word_lower[char_i]+query_word_lower[char_i+1]]:
                        if token_b not in suggestion_word_list_q:
                            suggestion_word_list_q[token_b] = 1
                        else:
                            suggestion_word_list_q[token_b] += 1
            suggestion_word_list_q_sorted = sorted(suggestion_word_list_q.items(), key=operator.itemgetter(1), reverse=True)
            if len(suggestion_word_list_q_sorted) > 0:
                irrelevant_flag = 0
                for character in irrelevant_characters:
                    if character in suggestion_word_list_q_sorted[0][0]:
                        irrelevant_flag = 1
                        break
                if irrelevant_flag == 0:
                    suggestion_word_list[query_word] = suggestion_word_list_q_sorted[0][0]
                    suggestion_string += suggestion_word_list_q_sorted[0][0] + " "
                else:
                    for i in range(1, len(suggestion_word_list_q_sorted)):
                        irrelevant_flag = 0
                        for character in irrelevant_characters:
                            if character in suggestion_word_list_q_sorted[i][0]:
                                irrelevant_flag = 1
                                break
                        if irrelevant_flag == 0:
                            suggestion_word_list[query_word] = suggestion_word_list_q_sorted[i][0]
                            suggestion_string += suggestion_word_list_q_sorted[i][0] + " "
                            break
            else:
                suggestion_word_list[query_word] = query_word
                suggestion_string += query_word + " "

    return suggestion_string.strip()


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


def hits_score(documents_list, d_id_list):
    reduced_binary_adjacency_matrix = [[0 for x in range(0, len(documents_list))] for y in range(0, len(documents_list))]
    document_index = 0
    for document in documents_list:
        link_index = 0
        for id_tuple in d_id_list:
            if urls[int(id_tuple[0])-1] in documents_list:
                reduced_binary_adjacency_matrix[document_index][link_index] = binary_adjacency_mat[urls.index(document)][int(id_tuple[0])-1]
                link_index += 1
        document_index += 1

    reduced_binary_adjacency_mat_transpose = matrix_transpose(reduced_binary_adjacency_matrix)

    query_hub_scores = {}
    query_authority_scores = {}

    hub_product_matrix = matrix_multiplication(reduced_binary_adjacency_matrix, reduced_binary_adjacency_mat_transpose)
    authority_product_matrix = matrix_multiplication(reduced_binary_adjacency_mat_transpose, reduced_binary_adjacency_matrix)
    hub_matrix_eigen_values = numpy.linalg.eigvals(hub_product_matrix)
    authority_matrix_eigen_values = numpy.linalg.eigvals(authority_product_matrix)
    hub_matrix_eigen_vector = numpy.linalg.eig(hub_product_matrix)
    hub_matrix_eigen_vector = hub_matrix_eigen_vector[1:][0]
    authority_matrix_eigen_vector = numpy.linalg.eig(authority_product_matrix)
    authority_matrix_eigen_vector = authority_matrix_eigen_vector[1:][0]

    hub_eig_val_count = 0

    for eigen_value_index in range(0, len(hub_matrix_eigen_values)):
        if numpy.absolute(numpy.absolute(hub_matrix_eigen_values[eigen_value_index]) - 1) < 0.2:
            hub_eig_val_count += 1
            for value_index in range(0, len(hub_matrix_eigen_vector[eigen_value_index])):
                if urls[int(d_id_list[value_index][0])-1] not in query_hub_scores:
                    query_hub_scores[urls[int(d_id_list[value_index][0])-1]] = numpy.absolute(hub_matrix_eigen_vector[eigen_value_index][value_index])
                else:
                    query_hub_scores[urls[int(d_id_list[value_index][0])-1]] += numpy.absolute(
                        hub_matrix_eigen_vector[eigen_value_index][value_index])

    for index in query_hub_scores:
        query_hub_scores[index] = query_hub_scores[index] / hub_eig_val_count

    authority_eig_val_count = 0

    for eigen_value_index in range(0, len(authority_matrix_eigen_values)):
        if numpy.absolute(numpy.absolute(authority_matrix_eigen_values[eigen_value_index]) - 1) < 0.2:
            authority_eig_val_count += 1
            for value_index in range(0, len(authority_matrix_eigen_vector[eigen_value_index])):
                if urls[int(d_id_list[value_index][0])-1] not in query_authority_scores:
                    query_authority_scores[urls[int(d_id_list[value_index][0])-1]] = numpy.absolute(
                        authority_matrix_eigen_vector[eigen_value_index][value_index])
                else:
                    query_authority_scores[urls[int(d_id_list[value_index][0])-1]] += numpy.absolute(
                        authority_matrix_eigen_vector[eigen_value_index][value_index])

    for index in query_authority_scores:
        query_authority_scores[index] = query_authority_scores[index] / authority_eig_val_count

    return query_hub_scores, query_authority_scores


print('Starting server...')

urls_file = open('./Search/Crawler/Files/urls.txt', 'r')

titles_file = open('./Search/Crawler/Files/titles.txt', 'r')

token_document_ii_file = open('./Search/Crawler/Files/token_document_ii.txt', 'r')

bigrams_file = open('./Search/Crawler/Files/bigrams.txt', 'r')

clusters_file = open('./Search/Clusters/Files/final_clusters.txt', 'r')

page_rank_file = open('./Search/PageRank/Files/page_rank.txt', 'r')

"""
hub_score_file = open('./Search/HITS analysis/Files/hub_score.txt', 'r')

authority_score_file = open('./Search/HITS analysis/Files/authority_score.txt', 'r')
"""

doc_adjacency_matrix_file = open('./Search/Crawler/Files/doc_adjacency_matrix.txt', 'r')

# token_document_matrix = {}
token_document_ii = {}

token_document_ii_file_list = token_document_ii_file.readlines()

for line in token_document_ii_file_list:
    if line[0] == '}' or (len(line) > 1 and line[len(line)-2]) == '{' or len(line) < 2:
        continue
    else:
        key = line[:line.index(' ')]
        values_list = line[line.index(' ')+2:len(line)-2]
        values = values_list.split('},')
        for value in values:
            if 'length' not in str(value):
                value_s = value[value.index('{')+1:len(value)-2]
                valuelr = value_s.split(',')
                value_l_key_value = valuelr[0].split(':')
                value_r_key_value = valuelr[1].split(':')
                value_l_key = value_l_key_value[0].strip().strip('\'')
                value_l_value = int(value_l_key_value[1].strip().strip('\''))
                value_r_key = value_r_key_value[0].strip().strip('\'')
                value_r_value = float(value_r_key_value[1].strip().strip('\''))
                if key not in token_document_ii:
                    token_document_ii[key] = [{value_l_key: value_l_value, value_r_key: value_r_value}]
                else:
                    token_document_ii[key] += [{value_l_key: value_l_value, value_r_key: value_r_value}]


urls = []

url_file_list = urls_file.readlines()

for url_line in url_file_list:
    if "{" in url_line or "}" in url_line:
        pass
    else:
        urls.append(url_line[:len(url_line)-1])

titles = {}

titles_file_list = titles_file.readlines()

for title_line in titles_file_list:
    if title_line[len(title_line)-2] == '{' or len(title_line) < 3:
        pass
    else:
        title_line_key_value = title_line.split(': ')
        title_line_key_value[0] = title_line_key_value[0].strip().strip('{').strip('\'')
        title_line_key_value[1] = title_line_key_value[1].strip().strip('}').strip('\'')
        if title_line_key_value[0] not in titles:
            titles[title_line_key_value[0]] = title_line_key_value[1]

bigrams = {}

bigrams_file_list = bigrams_file.readlines()

for bigram_line in bigrams_file_list:
    bigram_key_value = bigram_line.split(' = ')
    bigram_key_value[0] = bigram_key_value[0].strip()
    bigram_key_value[1] = bigram_key_value[1].strip().strip('[').strip(']')
    bigram_values = bigram_key_value[1].split(',')
    for i in range(len(bigram_values)):
        bigram_values[i] = bigram_values[i].strip().strip('\'')
    if bigram_values == ['']:
        bigrams[bigram_key_value[0]] = []
    else:
        bigrams[bigram_key_value[0]] = bigram_values

clusters = {}
cluster_names = {}

clusters_file_lines = clusters_file.readlines()
cluster_info = []
for line in clusters_file_lines:
    if line[0] == '{':
        line = line.strip().strip('\n').strip('}').strip('{')
        cluster_info = line.split(' ')
        clusters[cluster_info[0]] = []
        cluster_names[cluster_info[0]] = cluster_info[2]
    else:
        clusters[cluster_info[0]].append((line.strip().strip('\n'), titles[line.strip().strip('\n')]))

page_rank = {}

page_rank_lines = page_rank_file.readlines()

for line in page_rank_lines:
    if line[0] == 'P':
        pass
    else:
        page_rank[urls[int(line[:line.index(' ')])]] = float(line[line.index(' ')+1:])

"""

hub_score = {}

hub_score_lines = hub_score_file.readlines()

for line in hub_score_lines:
    if line[0] == 'H':
        pass
    else:
        hub_score[urls[int(line[:line.index(' ')])]] = float(line[line.index(' ')+1:])

authority_score = {}

authority_score_lines = authority_score_file.readlines()

for line in authority_score_lines:
    if line[0] == 'A':
        pass
    else:
        authority_score[urls[int(line[:line.index(' ')])]] = float(line[line.index(' ')+1:])

"""

adjacency_mat_lines = doc_adjacency_matrix_file.readlines()

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

for i in range(0, len(adjacency_mat)):
    for j in range(0, len(adjacency_mat[0])):
        if adjacency_mat[i][j] != 0:
            binary_adjacency_mat[i][j] = 1


print('Server started')
