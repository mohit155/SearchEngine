tokens_file = open('../Files/tokens.txt', 'r')
tokens = tokens_file.read()
tokens = tokens[tokens.index("{")+1:len(tokens)-6]
tokens = tokens[tokens.index("{")+1:]
tokens = tokens.split("\n")

bigrams = {}

for x in range(0, 26):
    for y in range(0, 26):
        bigrams[str(chr(x+97)+chr(y+97))] = []

for token in tokens:
    for bigram in bigrams:
        if bigram in token.lower():
            bigrams[bigram].append(token)

bigrams_file = open("../Files/bigrams.txt", "w")
for bigram_list in bigrams:
    bigrams_file.write(bigram_list + " = " + str(bigrams[bigram_list])+"\n")
