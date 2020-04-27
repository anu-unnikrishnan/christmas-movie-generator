from random import seed
from random import randint
from random import choices
from itertools import combinations

#separate paragraph input into words
"""
user_input = []
entry = input('\nEnter corpus ("#" on its own line to quit) : \n\n');
while entry != "#":
    user_input.append(entry)
    entry = input("")
corpus = '\n'.join(user_input)
"""

with open("/Users/anu/Documents/RC/Markov chains/Hallmark.txt", 'rb') as f:
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
distinct_words = list(set(corpus_words))
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

#then, we need to start building our transition matrix
#initialise a matrix of size [rows = distinct_block_words_count] X [cols = distinct_words_count] to zero
matrix = [0] * distinct_block_words_count
for i in range(distinct_block_words_count):
    matrix[i] = [0] * distinct_words_count

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

#to make it into the transition matrix, we need to normalise each row
transition_matrix = [0] * distinct_block_words_count
for i in range(distinct_block_words_count):
    transition_matrix[i] = [0] * distinct_words_count

for i in range(distinct_block_words_count):
    for j in range(distinct_words_count):
        #turn into probabilities
        if sum(matrix[i]) != 0:
            transition_matrix[i][j] = matrix[i][j]/sum(matrix[i])
        #because we don't want a divide-by-zero error
        else:
            transition_matrix[i][j] = matrix[i][j]

#seed random number generator
seed(None)

#we start by choosing a random block of words from all the distinct possible blocks
"""
flag = 0
while flag == 0:
    #pick a random block of words (we're picking the index here)
    x = randint(0, distinct_block_words_count)
    #if it's the last block of words, pick another one, because nothing follows that
    if x != distinct_block_words_count:
        flag = 1
    else:
        pass
"""

max_words = int(input('\nHow many words do you want to generate? '))
no_words = 1
sentence = []

#add our starting block to our sentence
#sentence.append(distinct_block_words[x])

#start from 'a woman'
sentence.append(distinct_block_words[0])
x = 0
#sentence now consists of a sublist of a list, so join those together
sentence = [' '.join(l) for l in sentence]

#print("\nWe start from block", distinct_block_words[x])

#generate max_words words
while no_words <= max_words:

    #this has generated a random index x
    #let's now look at the row of x and pick the next word with corresponding probability
    weights = []
    population = []
    
    #extract out the probabilities corresponding to that word (row x of transition_matrix)
    for i in range(distinct_words_count):
        j = transition_matrix[x][i]
        weights.append(j)
        population.append(i)

    #here we are making our new block, which consists of the new word preceded by (k-1) words in the previous block
    #first we add the words of the previous block except its first word
    next_block = []
    this = distinct_block_words[x]
    for i in range(1, len(this)):
        next_block.append(this[i])

    #if all weights are zero, we just end the sentence, because this means there are no words following our previous block
    #if we didn't end the sentence, choices() would just always choose the last element
    check = 0
    for i in weights:
        if i != 0:
            check = 1
        else:
            pass
    #if all weights are zero
    if check == 0:
        break
    else:
        pass

    #choose an element from population, each of which has corresponding weight
    draw = choices(population, weights)
    #draw gives a single list element, so let's just make this an int by taking the first (and only) list element
    x = draw[0]
    #print("The next word is", distinct_words[x])

    #adding the new word to our sentence
    sentence.append(distinct_words[x])

    #finishing off the creation of our next block
    next_block.append(distinct_words[x])

    #print("The next block is", next_block, "\n")

    #if our next block isn't in the corpus, we don't generate more text
    if next_block not in distinct_block_words:
        break
    else:
        pass

    #now we need to go from this block to figure out our next word
    x = distinct_block_words.index(next_block)

    #break if it's started a new plot
    if distinct_block_words[x] == ['a', 'woman']:
        sentence = sentence[:len(sentence)-2] #gets rid of 'a woman' from already started new plot 
        break

    #keep track of how many words in our sentence
    no_words += 1

final_text = ' '.join(sentence)

final_text = final_text.replace(' " ', "'' " )
final_text = final_text.replace('"', " '' ")
final_text = final_text.replace(' , ', ', ')
final_text = final_text.replace(' . ', '. ')
final_text = final_text.replace(' ! ', '! ')
final_text = final_text.replace(' ? ', '? ')
final_text = final_text.replace(' ^ ', '\n')
final_text = final_text.replace(' £ ', '\n\n')

sent_list = final_text.split('\n')
cap_text = "\n".join((j.capitalize() for j in sent_list))
cap_text = cap_text.replace(' i ', ' I ')
cap_text = cap_text.replace(" i'", " I'")
cap_text = cap_text.replace("'cause", "'Cause")

print('\nYour new sentence is :\n\n', '...', cap_text, '...\n')















