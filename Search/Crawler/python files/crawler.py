from urllib import error
from urllib import request
import math
import numpy

from my_html_parser import MyHTMLParser
import constant
import graph_plot
import file_writer


# seed_url = "https://mva.microsoft.com"
# seed_url = "https://docs.python.org/3.5/library/urllib.request.html#module-urllib.request"
# seed_url = "https://www.codechef.com/"
# seed_url = "https://www.tutorialspoint.com/"
seed_url = "https://en.wikipedia.org/wiki/Main_Page"


main_unique_urls = []
main_unique_urls_title = []
main_tokens = []
main_token_document_ii = {}
main_token_document_matrix = {}

main_url_in_degree = {}

main_url_out_degree = {}

main_doc_adjacency_mat = [[0 for xa in range(0, constant.pages)] for ya in range(0, constant.pages)]

main_temp_document_token = {}


def get_links(param_url, j):
    global main_tokens
    global main_temp_document_token
    global main_doc_adjacency_mat
    global main_unique_urls
    global main_unique_urls_title

    main_temp_document_token = {}

    parser = MyHTMLParser(main_tokens, main_temp_document_token, main_doc_adjacency_mat, main_unique_urls, main_unique_urls_title)
    print("Total Unique urls = " + str(len(main_unique_urls))+" Current url number= " + str(j))
    print("Establishing connection with "+param_url)
    response_code = 404
    response = " "
    try:
        parser.init_url(param_url)
        response = request.urlopen(param_url)
        response_code = response.getcode()
    except error.HTTPError:
        print("Could not make connection with url " + param_url + " HTTPError response code is not 200")
    except TimeoutError:
        print("Could not make connection with url " + param_url + " TimeoutError ")
        response_code = -1
    except error.URLError:
        print("Could not make connection with url " + param_url + " TimeoutError ")
        response_code = -1
    if response_code == 200:
        url_text = response.read()
        print("Parsing...")
        parser.feed(str(url_text))
        
        main_tokens = parser.tokens
        main_temp_document_token = parser.temp_document_token
        main_doc_adjacency_mat = parser.doc_adjacency_mat
        main_unique_urls = parser.unique_urls
        main_unique_urls_title = parser.unique_urls_title


i = 1


def mat():
    global main_temp_document_token

    if len(main_token_document_ii) == 0:
        for token in main_temp_document_token:
            main_token_document_ii[token] = [{i: main_temp_document_token[token]}]
            main_token_document_matrix[token] = [main_temp_document_token[token]]
    else:
        for doc_token in main_token_document_ii:
            if doc_token in main_temp_document_token:
                main_token_document_ii[doc_token] += [{i: main_temp_document_token[doc_token]}]
                main_token_document_matrix[doc_token] += [main_temp_document_token[doc_token]]
            else:
                main_token_document_matrix[doc_token] += [0]
        for doc_token in main_temp_document_token:
            if doc_token not in main_token_document_ii:
                main_token_document_ii[doc_token] = [{i: main_temp_document_token[doc_token]}]
                main_token_document_matrix[doc_token] = [0]
                for x in range(1, i):
                    main_token_document_matrix[doc_token] += [0]
                    main_token_document_matrix[doc_token] += [main_temp_document_token[doc_token]]

main_unique_urls.append(seed_url)
get_links(seed_url, 0)
mat()


while 1:
    # if len(unique_urls) < 1000:

    if i < constant.pages:
        if i < len(main_unique_urls):
            param_url1 = main_unique_urls[i]
            get_links(param_url1, i+1)
            i += 1
            mat()
        else:
            break
    else:
        break

for temp_doc_token in main_token_document_ii:
    main_token_document_ii[temp_doc_token] += [{"length": len(main_token_document_ii[temp_doc_token])}]
    for doc_token_freq in main_token_document_ii[temp_doc_token]:
        key = list(doc_token_freq.keys())
        if key[0] != 'length':
            doc_token_freq["TFID"] = -doc_token_freq[key[0]]*math.log(len(main_token_document_ii[temp_doc_token])/constant.pages)


l = len(main_token_document_matrix)
print("number of tokens = "+str(l))
token_document_mat = [[0 for x in range(0, constant.pages)] for y in range(0, l)]
token_document_mat_transpose = [[0 for x1 in range(0, l)]for y1 in range(0, constant.pages)]
Q = [[0 for x2 in range(0, constant.pages)]for y2 in range(0, constant.pages)]
U = [[0 for x3 in range(0, constant.pages)]for y3 in range(0, constant.pages)]
trace_q = 0
trace_q_diagonal = 0

eigen_values = []
eigen_vector = []


def post_computation():
    global eigen_values
    global trace_q
    global trace_q_diagonal
    global eigen_vector

    print('Computing matrix. This might take some time. Please wait...')

    t = 0
    for item in main_token_document_matrix:
        j1 = 0
        print(t, len(main_token_document_matrix[item]), end=' ')
        if t % 1000 == 0:
            print()
        for x in main_token_document_matrix[item]:
            token_document_mat[t][j1] = x
            token_document_mat_transpose[j1][t] = x
            j1 += 1
            if j1 > constant.pages-1:
                print('violation', j1)
                break
        t += 1

    print('matrix computed.')
    print('Computing eigen values and vector. This might take some time. Please wait...')

    for itr in range(0, constant.pages):
        print(itr)
        for itr1 in range(0, constant.pages):
            for itr2 in range(0, l):
                Q[itr][itr1] += token_document_mat_transpose[itr][itr2]*token_document_mat[itr2][itr1]
            if itr == itr1:
                trace_q += Q[itr][itr1]

    eigen_values = numpy.linalg.eigvals(Q)
    eigen_vector = numpy.linalg.eig(Q)
    eigen_vector = eigen_vector[1:]

    for itr in range(0, constant.pages):
        for itr1 in range(0, constant.pages):
            U[itr][itr1] = eigen_vector[0][itr][itr1]

    print(U)

    q_diagonal = [[0 for x4 in range(0, constant.pages)] for y4 in range(0, constant.pages)]

    for i11 in range(0, constant.pages):
        for j11 in range(0, constant.pages):
            if i11 == j11:
                q_diagonal[i11][j11] = eigen_values[i11]
                trace_q_diagonal += eigen_values[i11]

    print("eigen values =")
    print(eigen_values)
    print("Q_diagonal =")
    print(q_diagonal)
    print("trace_q = " + str(trace_q) + " trace_q_diagonal= " + str(trace_q_diagonal))

# post_computation() # lsa
# file_writer.write_mat(l, constant.pages, token_document_mat, token_document_mat_transpose, Q)
file_writer.write_urls(main_unique_urls)
file_writer.write_titles(main_unique_urls_title)
file_writer.write_tokens(main_tokens)
file_writer.write_token_document_ii(main_token_document_ii, main_token_document_matrix)
file_writer.write_doc_adjacency_matrix(main_doc_adjacency_mat)

sum_noise = 0


def noise():
    global sum_noise
    global Q
    itr = 0
    for itr in range(0, constant.pages):
        sum_noise += Q[itr][itr]
        if sum_noise/trace_q > .8:
            break
    print("k="+str(itr)+" sum = "+str(sum_noise)+" ratio = "+str(sum_noise/trace_q))

# noise()

# graph_plot.plot_graph(eigen_values, constant.pages)


print("doc adjacency matrix")

for i in range(0, constant.pages):
    print(str(main_unique_urls[i]) + " ", end='')

print()

for i in range(0, constant.pages):
    print(str(main_unique_urls[i]) + " ", end='')
    for j2 in range(0, constant.pages):
        print(str(main_doc_adjacency_mat[i][j2]) + " ", end='')
    print()

print("Done.")
