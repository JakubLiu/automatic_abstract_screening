import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

"""
Downloads that need to be run only once:

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
"""


"""
input:
    a string
output:
    a list of tokens
description:
    This function removes all punctuation marks and whitespaces from a sentence and stores the sentence as a list of tokens (strings).
    Optionally you can also remove digits (by default the function does not remove them).
"""
def tokenize(input_sentence, remove_digits = False):
    tokens_raw=word_tokenize(input_sentence)
    tokens_clean = []
    for token in tokens_raw:
        if remove_digits == False:
            cleaned_token = (re.sub(r'[^\w\s]', '', token))
        else:
            cleaned_token = re.sub(r'[^\w\s]|[0-9]', '', token)
        if cleaned_token != '':
            tokens_clean.append(cleaned_token)
    return tokens_clean

"""
example usage:
    >x = tokenize('Noovera jest, bardzo śmieszna !!', remove_digits=False)
    >print(x)
    >['Noovera', 'jest', 'bardzo', 'śmieszna']
"""





"""
input:
    a list of tokens
output:
    a list of tokens without stop words
description:
    This function removes stop words like 'the' or 'is'. The user needs to choose the language from which the stopwords come.
"""
def remove_stopwords(tokenized_sentence, language):
    stop_words = set(stopwords.words(language))
    no_stopwords = []
    
    for token in tokenized_sentence:
        if token.lower() not in stop_words:
            no_stopwords.append(token)
    
    return no_stopwords

"""
Example usage:
    >x = remove_stopwords(['Noovera', 'is', 'the', 'most', 'medium-sized', 'feline'], language='english')
    >print(x)
    >['Noovera', 'medium-sized', 'feline']
"""






"""
input:
    a list of tokens with no stop words
output:
    a list of stemmed tokens
description:
    This function stemms each token. Example: 'running' -> 'run'.
"""
def stemming(tokenized_sentence):
    ps = PorterStemmer()
    stemmed_sentence = []

    for token in tokenized_sentence:
        stemmed_token = ps.stem(token, to_lowercase=True)
        stemmed_sentence.append(stemmed_token)
    
    return stemmed_sentence

"""
Example usage:
    >x = stemming(['Noovera', 'constantly', 'swimming', 'hunting', 'constatly'])
    >print(x)
    >['noovera', 'constantli', 'swim', 'hunt', 'constatli']
"""

"""
A wrapper function for the above functions.
"""
def text_preprocessing_wrapper(input_sentence, rm_digit = False, language = 'english'):
    x1 = tokenize(input_sentence, remove_digits = rm_digit)
    x2 = remove_stopwords(x1, language = language)
    x3 = stemming(x2)
    return x3
"""
Example usage:
    >res = text_preprocessing_wrapper('Noovera is very funny 10 swimming', rm_digit=True, language='english')
    >print(res)
    >['noovera', 'funni', 'swim']
"""