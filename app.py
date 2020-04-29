from flask import Flask, request, render_template
from random import seed
from random import randint
from random import choices
from itertools import combinations
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/christmas', methods=['GET', 'POST'])
def divide():
    result = None
    if request.method == 'POST':
        #input_text = str(request.form['input_text']) #input text
        #how_many_words = float(request.form['how_many_words']) #how many words 

        with open("plots.txt", 'rb') as f:
            lines = [l.decode('utf8', 'ignore') for l in f.readlines()]
        corpus = "".join(lines)

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

        """
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
        """

        #load transition matrix that was previously created
        transition_matrix = np.load("transitionmatrix.npy")

        #seed random number generator
        seed(None)

        plotgenerated = 0
        sentence = []

        #add our starting block to our sentence
        #sentence.append(distinct_block_words[x])

        #start from 'a woman'
        sentence.append(distinct_block_words[0])
        x = 0
        no_words = 2

        #sentence now consists of a sublist of a list, so join those together
        sentence = [' '.join(l) for l in sentence]

        #print("\nWe start from block", distinct_block_words[x])

        #generate one plot 
        while plotgenerated == 0:

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

            no_words += 1

            #break if we've finished a sentence and gone over 180 words
            if distinct_words[x] == '.' and no_words >= 180:
                break

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
                plotgenerated = 1
                break

        final_text = ' '.join(sentence)

        final_text = final_text.replace(' " ', "'' " )
        final_text = final_text.replace('"', " '' ")
        final_text = final_text.replace(' , ', ', ')
        final_text = final_text.replace(' . ', '. ')
        final_text = final_text.replace(' ! ', '! ')
        final_text = final_text.replace(' ? ', '? ')
        final_text = final_text.replace(' ^ ', '<br>')
        final_text = final_text.replace(' £', '')

        sent_list = final_text.split('\n')
        cap_text = '<br>'.join((j.capitalize() for j in sent_list))

        #capitalise first word of every sentence 
        resarray = []
        new_cap_text = cap_text.split('.')
        for i in new_cap_text:
            resarray.append(i.strip().capitalize()+". ")

        cap_text = ''.join(resarray)

        #process final text depending on words that we know are present in the input
        cap_text = cap_text.replace('havent', "haven't")
        cap_text = cap_text.replace('wasnt', "wasn't")
        cap_text = cap_text.replace('doesnt', "doesn't")
        cap_text = cap_text.replace('wont', "won't")
        cap_text = cap_text.replace("christmas", "Christmas")
        cap_text = cap_text.replace("nick", "Nick")
        cap_text = cap_text.replace(" shes ", " she's ")
        cap_text = cap_text.replace(" hes ", " he's ")
        cap_text = cap_text.replace("american", "American")
        cap_text = cap_text.replace("european", "European")
        cap_text = cap_text.replace("vermont", "Vermont")
        cap_text = cap_text.replace("boston", "Boston")
        cap_text = cap_text.replace("virginia", "Virginia")
        cap_text = cap_text.replace("alaska", "Alaska")
        cap_text = cap_text.replace("new york", "New York")
        cap_text = cap_text.replace("fathers", "father's")
        cap_text = cap_text.replace("mothers", "mother's")
        cap_text = cap_text.replace("ceo", "CEO")
        cap_text = cap_text.replace("towns", "town's")
        cap_text = cap_text.replace(" kings ", " king's ")
        cap_text = cap_text.replace('. .', '.')
        cap_text = cap_text.replace('?.', '?')
        cap_text = cap_text.replace('^.', '')

        result = cap_text

    return render_template('divide.html', result=result)

if __name__ == '__main__':
    app.debug = True
    app.run()