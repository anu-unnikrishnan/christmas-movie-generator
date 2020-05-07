
Guide to building Markov chains to create Christmas movie plots.
--------------------------------------------------------------------

This repository contains Python code for constructing Markov chains using some given text.

1) Markov-Chain.py - building a Markov chain that can be applied to some input text to generate new, similar-sounding text. 
2) Hallmarkov.py - a Markov chain adapted to generate Christmas movie plots. Instead of choosing a random word to start the text generation from, we always start from 'a woman', to give more sensible plots.
3) plots.txt - file containing real Christmas movie plots that functions as the 'corpus' or input text.
4) app.py - python code using Flask to create a web app.
6) process_files.py - creating and saving transition matrix to save time every time a new plot is generated using same corpus.
7) transition_matrix.npy - transition matrix created in process_files.py stored as a numpy 2D matrix.

A Markov chain allows us to transition between states. Each transition occurs with a certain probability. The next state only depends on the current state - this is the Markov property - it has no memory of the previous states.

In our case, each state is a word. We start with k = 1. This means that we take each word, see what possible words can come after it, and with what probabilities they occur. Then, we choose the next word depending on these probabilities.

The probabilities are entered into a transition matrix. Our first step is to determine this matrix. So, we take the sample text (the corpus), separate it into unique or distinct words, and make a transition matrix of zeros of size (distinct_words) X (distinct_words). Each row of the matrix and each column corresponds to a particular distinct word. Then, we add a 1 to the element of each row that corresponds to a word that follows the word of that row. So, each row corresponds to a particular word, and we add a 1 every time the column word follows it. 

In this way, we build up a transition matrix. Then, we normalise each row to get probabilities - so we divide the elements in each row by the sum of the elements in that row. 

Our next step is to choose a word at random from the distinct words. We then want to see what it transitions to. We go to the relevant row of our transition matrix that corresponds to this word - then we pick a word at random from the probability distribution by using a weighted random choice function. 

We then start from this new word, and pick the next word from its probability distribution. We keep going like this until we have generated the required number of words. 

Similarly, when k = 2, we consider blocks of two words and see which words come after each block. This allows us to create more sensible-sounding/less random text.

Note that k can be increased to whatever we want, but as k increases the text will start resembling the corpus more and more.
