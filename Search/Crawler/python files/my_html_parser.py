from html.parser import HTMLParser
import nltk
import constant


class MyHTMLParser(HTMLParser):
    url = " "
    current_directory_url = " "
    parent_directory_url = " "
    url_till_hash = " "
    root_url = " "
    last_tag = " "
    
    unique_urls = []
    unique_urls_title = []
    tokens = []
    temp_document_token = {}
    doc_adjacency_mat = [[0 for xa in range(0, constant.pages)] for ya in range(0, constant.pages)]

    def __init__(self, tokens, temp_document_token, doc_adjacency_mat, unique_urls, unique_urls_title):
        HTMLParser.__init__(self)
        self.unique_urls = unique_urls
        self.tokens = tokens
        self.temp_document_token = temp_document_token
        self.doc_adjacency_mat = doc_adjacency_mat
        self.unique_urls_title = unique_urls_title

    def init_url(self, param_url):
        self.url = param_url
        last_slash = self.url.rfind("/")  # print(last_slash)
        self.current_directory_url = self.url[:last_slash + 1]  # print(current_directory_url)
        second_last_slash = self.url.rfind("/", 0, self.url.rfind("/"))  # print(second_last_slash)
        self.parent_directory_url = self.url[:second_last_slash + 1]  # print(parent_directory_url)
        hash_index = self.url.rfind("#")  # print(hash_index)
        if hash_index == -1:
            hash_index = len(self.url)
        self.url_till_hash = self.url[:hash_index]  # print(url_till_hash) # print()
        self.root_url = self.url[:self.url.find("/", self.url.find("/")+2)+1]
        # print("      root_url  "+self.root_url+"    ")

    def error(self, message):
        pass

    def handle_starttag(self, tag, attributes):
        self.last_tag = tag
        if tag == "a":
            for attr in attributes:
                if attr[0] == 'href':
                    new_url = ""
                    if attr[1].startswith("../"):
                        new_url = attr[1].replace("../", self.parent_directory_url, 1)
                    elif attr[1].startswith("./"):
                        new_url = attr[1].replace("./", self.current_directory_url, 1)
                    elif attr[1].startswith("//"):
                        new_url = attr[1].replace("/", "https:/", 1)
                    elif attr[1].startswith("/"):
                        new_url = attr[1].replace("/", self.root_url, 1)
                    else:
                        if not attr[1].startswith("http"):
                            if attr[1].startswith("#"):
                                new_url = self.url
                                '''
                                new_url = self.url_till_hash + attr[1]
                                '''
                            else:
                                new_url = self.current_directory_url+attr[1]
                        else:
                            new_url = attr[1]
                    if new_url.endswith(".webm") or new_url.endswith(".ogg") or new_url.endswith(".ogv") or new_url.endswith(".mp4") or new_url.endswith(".jpeg") or new_url.endswith(".jpg") or new_url.endswith(".png") or new_url.endswith(".gif"):
                        pass
                    else:
                        if new_url not in self.unique_urls and len(self.unique_urls) < constant.max_urls:
                            self.unique_urls.append(new_url)
                        if new_url in self.unique_urls and self.unique_urls.index(new_url) < constant.pages:
                            self.doc_adjacency_mat[self.unique_urls.index(self.url)][self.unique_urls.index(new_url)] += 1

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.last_tag != "script" and self.last_tag != "style":
            text = str(data)
            # text_split = text.split(" ")
            text_split = nltk.word_tokenize(text)
            for x in text_split:
                if x not in self.tokens:
                    self.tokens.append(x)
                if x not in self.temp_document_token:
                    self.temp_document_token[x] = 1
                else:
                    self.temp_document_token[x] += 1
        if self.last_tag == 'title' or self.last_tag == 'Title':
            text_t = str(data)
            self.unique_urls_title.append({self.url: text_t})
            pass
