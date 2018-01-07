import datetime
import constant
'''
titles list \\n
'''


def write_urls(unique_urls):
    print("Writing to file...")
    url_file = open('../Files/urls.txt', 'w')
    date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    url_file.write("urls on ["+date+"]{\n")
    url_file.write("unique urls [size:"+str(len(unique_urls))+"] {\n")

    for x in unique_urls:
        url_file.write(str(x)+"\n")

    url_file.write("}\n}\n\n")
    url_file.close()


def write_titles(unique_urls_titles):
    print("Writing to file...")
    titles_file = open('../Files/titles.txt', 'w')
    date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    titles_file.write("Titles on ["+date+"]{\n")
    titles_file.write("url Titles [size:"+str(len(unique_urls_titles))+"] {\n")

    for x in unique_urls_titles:
        titles_file.write(str(x)+"\n")

    titles_file.write("}\n}\n\n")
    titles_file.close()


def write_tokens(tokens):
    print("Writing tokens to file...")
    tokens_file = open('../Files/tokens.txt', 'w')
    date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    tokens_file.write("Tokens on ["+date+"]{\n")
    tokens_file.write("unique Tokens [size:"+str(len(tokens))+"(the actual words may be less because of unicode)] {\n")
    for x in tokens:
        try:
            tokens_file.write(x+"\n")
        except UnicodeEncodeError:
            pass
    tokens_file.write("}\n}\n\n")
    tokens_file.close()


def write_token_document_ii(token_document_ii, token_document_matrix):
    max_freq = 0
    max_freq_token = ""
    print("Writing token document matrix to file...")
    tokens_file = open('../Files/token_document_ii.txt', 'w')
    date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    tokens_file.write("Tokens on ["+date+"]{\n")

    tokens_matrix_file = open('../Files/token_document_matrix.txt', 'w')
    date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    tokens_matrix_file.write("Tokens on [" + date + "] size[" + str(len(token_document_matrix)) + "][100] {\n")

    for token in token_document_ii:
        try:
            tokens_file.write(str(token)+" "+str(token_document_ii[token])+"\n")
        except UnicodeEncodeError:
            pass
    for token in token_document_matrix:
        try:
            tokens_matrix_file.write(str(token) + " " + str(token_document_matrix[token]) + "\n")
        except UnicodeEncodeError:
            pass
        if max_freq < len(token_document_ii[token]):
            max_freq = len(token_document_ii[token])
            max_freq_token = token
    tokens_file.write("}\n\n")
    print("maximum freq token is " + max_freq_token + "." + str(max_freq-1))
    tokens_file.close()


def write_mat(l, pages, token_document_mat, token_document_mat_transpose, Q):
    matrix_file = open('../Files/matrix.txt', 'w')
    matrix_file.write("token document matrix ["+str(l)+"][100]\n")
    for i1 in range(l):
        matrix_file.write("[ ")
        for j in range(pages):
            matrix_file.write(str(token_document_mat[i1][j])+" ")
        matrix_file.write("]\n")
    matrix_file.write("\n\ntoken document matrix  transpose [100][" + str(l) + "]\n")
    for i1 in range(pages):
        matrix_file.write("[ ")
        for j in range(l):
            matrix_file.write(str(token_document_mat_transpose[i1][j])+" ")
        matrix_file.write("]\n")
    matrix_file.close()
    matrixq_file = open('../Files/matrixq.txt', 'w')
    matrixq_file.write("token document matrix [" + str(l) + "][100]\n")
    for i10 in range(pages):
        matrixq_file.write("[ ")
        for j10 in range(pages):
            matrixq_file.write(str(Q[i10][j10]) + " ")
        matrixq_file.write("]\n")


def write_doc_adjacency_matrix(doc_adjacency_matrix):
    doc_adjacency_matrix_file = open('../Files/doc_adjacency_matrix.txt', 'w')
    doc_adjacency_matrix_file.write('Document adjacency matrix' + "\n")
    print("Writing Adjacency matrix to file...")
    for i in range(constant.pages):
        doc_adjacency_matrix_file.write(str(doc_adjacency_matrix[i])+"\n")
