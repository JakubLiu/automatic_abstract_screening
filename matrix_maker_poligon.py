import numpy as np
import pubmed_search
import text_preprocessing
import pandas as pd
import csv

'''
# Here we create the csv file based on the keyword. But we don't need to run that here.

pubmed_search.enter_email()  # enter email for entrez
id_list = pubmed_search.search_pubmed('European Brown Bear', operator='AND', database='pubmed')  # get paper IDs

# for diagnostic purposes only proceed with 10 first IDs
id_list_short = id_list[:10]
pubmed_search.get_abstracts(id_list_short, save_csv=True)  # save doi numbers and abstracts as csv
'''


file = pd.read_csv("paper_dict.csv")  # read csv file
dictionary = file.set_index(file.columns[0])[file.columns[1]].to_dict()   # convert df back to dictionary
# the keys are the doi numbers
# the values are the abstract texts

# build vocabulary________________________________________________________________________________________________________
"""
    - each column corresponds to a word from the vocabulary
    - each row corresponds to an abstract
    - we must change the vocabulary from set() to list() to preserve the ordering
    - somehow we must map column numbers of the array to the words, because the array will be of type float
"""
vocabulary = set()  # this set will hold all the tokens across all abstracts
tokenized_abstracts = []

for ab in dictionary.values():     # dictionary.values() --> abstracts
    ab_processed = text_preprocessing.text_preprocessing_wrapper(ab, rm_digit=True, language='english')
    tokenized_abstracts.append(ab_processed)
    
    for token in ab_processed:  # add each token to the vocabulary
        vocabulary.add(token)
#________________________________________________________________________________________________________________________

# build frequency matrix______________________________________________________________________________________________
n_abstracts = len(dictionary.values())
vocab_size = len(vocabulary)
freq_matrix = np.zeros((n_abstracts, vocab_size), dtype = np.float16)

# build a dictionary which maps each doi to the row number of the feature matrix
doi_rownum_dict = {}
rownum = 0
for doi in dictionary.keys():
    doi_rownum_dict[doi] = rownum
    rownum = rownum + 1


vocabulary = list(vocabulary)   # convert set to list to not loose the ordering
for i in range(0, len(tokenized_abstracts)):   # iterate over the abstracts
    for j in range(0, vocab_size):     # iterate over the tokens
        if vocabulary[j] in tokenized_abstracts[i]:
            count = tokenized_abstracts[i].count(vocabulary[j])  # count the number of times the given token appears in the given abstract
            length = len(tokenized_abstracts[i])      # this is the lenght of the abstract
            freq_matrix[i][j] = count/length         # calculate the frequency and store it in the feature matrix



np.savetxt('frrequency_featrue_matrix.txt', freq_matrix, fmt = '%5.10f')
print('all done.')
"""
# Sanity checks

print(freq_matrix[0][:])
print('_______________________________')
print(tokenized_abstracts[0])
print('_______________________________')

print(vocabulary)
print('_______________________________')

print(doi_rownum_dict.keys())
print(tokenized_abstracts[0])
"""

print(np.sum(freq_matrix[0][:]))