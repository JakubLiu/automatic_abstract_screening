from Bio import Entrez
import pandas as pd
import numpy as np
from metapub import FindIt
import csv

 
#Entrez.email = "jakub-jozef.liu@charite.de"


def enter_email():
    Entrez.email = str(input("Enter email: "))

 
# searches the given db for the keyword(s) connected with the given logic operator
# returns a np array of entrez IDs
def search_pubmed(keyword, operator, database):

    # modify keyword according to logic operator
    insert = ' ' + operator + ' '
    
    keyword = keyword.replace(' ', insert)

    # Search for articles in the db
    handle = Entrez.esearch(db=database, term=keyword, retmax=100)
    record = Entrez.read(handle)
    handle.close()
    
    id_array = np.zeros(len(record['IdList']), dtype = int)
    for i in range(0, id_array.shape[0]):
        id_array[i] = int(record['IdList'][i])

    return id_array


# input: list of paper IDs
# output: dictionary of the form: {doi:abstract}
# optional output: dictionary saved as csv
def get_abstracts(ID_list, save_csv = False):
    total_len = ID_list.shape[0]
    i = 0
    paper_dict = {}
    for pmid in ID_list:
        print(np.round(i/total_len, 2), 'done.')
        i = i + 1
        src = FindIt(pmid)
        abstract = src.pma.abstract
        doi = src.pma.doi
        paper_dict[doi] = abstract

    if save_csv == True:
        print('saving csv...')
        with open('paper_dict.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Key", "Value"])
            for key, value in paper_dict.items():
                writer.writerow([key, value])
        print('csv saved.')
    
    return paper_dict




"""
# Main_____________________________________________________________________________________________________
keyword = "is"

# this works fine
id_list = search_pubmed(keyword, operator='AND', database='pubmed')
print(id_list)
#my_dict = get_abstracts(id_list, save_csv=True)
print('all done.')

"""


