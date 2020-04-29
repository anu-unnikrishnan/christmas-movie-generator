from random import seed
from random import randint
from random import choices
from itertools import combinations
import numpy as np

#separate paragraph input into words

with open("/Users/anu/Documents/RC/Markov chains/plots.txt", 'rb') as f:
     lines = [l.decode('utf8', 'ignore') for l in f.readlines()]

corpus = "".join(lines)
print(corpus)

corpus = corpus.lower()

corpus = corpus.replace('\n', ' ^ ')
corpus = corpus.replace(' ^  ^ ', ' £ ')
corpus = corpus.replace(',', ' , ')
corpus = corpus.replace('.', ' . ')
corpus = corpus.replace('!', ' ! ')
corpus = corpus.replace('?', ' ? ')

#this gives us a list of the words in the corpus (punctuation is considered a word)
corpus_words = corpus.split(' ')
corpus_words = [word for word in corpus_words if word != '']

#separate the full set of corpus words into distinct words
#distinct_words = list(set(corpus_words))
distinct_words = []
for i in corpus_words:
    if i not in distinct_words:
        distinct_words.append(i)
distinct_words_count = len(distinct_words)

#train the chain
#k is the number of words our chain will consider before predicting the next one
k = 2

#if k is greater than 1, our transition matrix will consist of rows corresponding to distinct blocks of k words, and columns corresponding to distinct words
#eg. corpus_words[0:1] will give corpus_words[0], corpus_words[0:2] will give [corpus_words[0] corpus_words[1]]
block_words = [corpus_words[i:i+k] for i in range(len(corpus_words)-k+1)]

#extracting out the unique blocks and storing in distinct_block_words
distinct_block_words = []
for i in block_words:
    if i not in distinct_block_words:
        distinct_block_words.append(i)
distinct_block_words_count = len(distinct_block_words)

matrix = np.zeros(shape = (distinct_block_words_count, distinct_words_count))

#go up to the last-but-one block of words
for i in range(len(block_words)-1):
    #look at the next word in the corpus, find its index in distinct_block_words
    #add one to the element in:
    #the row corresponding to the index of the i^th block of words in the corpus, and
    #the column corresponding to the index of the (i+k)^th word in the corpus
    #this works because finding the next word after block_words means we go to the (i+k)^th element of corpus_words
    #note that both block_words and corpus_words are in order
    #we find the index of that word in distinct_block_words and distinct_words because
    matrix[distinct_block_words.index(block_words[i])][distinct_words.index(corpus_words[i+k])] += 1

transition_matrix = np.zeros(shape = (distinct_block_words_count, distinct_words_count))

for i in range(distinct_block_words_count):
    for j in range(distinct_words_count):
        #turn into probabilities
        if sum(matrix[i]) != 0.0:
            transition_matrix[i][j] = matrix[i][j]/sum(matrix[i])
        #because we don't want a divide-by-zero error
        else:
            transition_matrix[i][j] = matrix[i][j]

#save transition matrix to file 
np.save('/Users/anu/Documents/RC/Markov chains/transitionmatrix.npy', transition_matrix)










