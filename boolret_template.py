#!/usr/bin/env python

#########################################################################
# Data Programming - MSc in Data Science 2018 - Assignment 1/2
# Author: KOUTSOUMPOS ISIDOROS
#########################################################################

import sys
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re,json,os

CRAN_COLL = './cran.all.1400'
INDEX_FILE = 'cran.ind'

SYMBOLS = '!@#$%^&*()[]{};\':",.<>/?`~-_=+'


def parse_documents(cran_file=CRAN_COLL):
    """Parse the document body and title fields of the Cranfield collection.
    Arguments:
        cran_file: (str) the path to the Cranfield collection file
    Return:
        (body_kwds, title_kwds): where body_kwds and title_kwds are
        dictionaries of the form {docId: [words]}.
    """
    document = open(cran_file,'r')
    lines = document.readlines()
    docDict = {}
    titleDict = {}

    global id
    for i in range(0,len(lines)):
        if lines[i].startswith('.I'):
            linesplit = lines[i].split()
            id = int(linesplit[1])

        titlesList = []
        if lines[i].startswith('.T') :
            while not lines[i+1].startswith('.A'):
                linesplit = lines[i+1].split('\n')
                titles = linesplit[0]
                titlesList.append(titles)
                titleDict[id] = titlesList
                i+=1
        del titlesList

        if lines[i].startswith('.A'):
            linesplit = lines[i+1].split('\n')

            if linesplit[0].startswith('.B'):
                author = ''
            else:
                author = linesplit[0]

        if lines[i].startswith('.B'):
            linesplit = lines[i+1].split('\n')
            if linesplit[0].startswith('.W'):
                book = ''
            else:
                book = linesplit[0]

        if lines[i].startswith('.W'):
            if lines[i+1].startswith('.I'):
                pass #print "not a word"
            else:
                try:
                    lista = []
                    while not lines[i+1].startswith('.I'):
                        x = lines[i+1].split('\n')
                        lista.append(x[0].rstrip())
                        i+=1
                        docDict[id] = lista
                    del lista
                except IndexError:
                    pass
    document.close()
    return docDict,titleDict

def pre_process(words):
    """Preprocess the list of words provided.
    Arguments:
        words: (list of str) A list of words or terms
    Return:
        a shorter list of pre-processed words
    """
    # Get list of stop-words and instantiate a stemmer:
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    finalList = []
    otherList = []
    for i in words:
        stringsSplittedList = i.split()
        proxeirhlista = []

        for string in (stringsSplittedList):
            #### Remove symbols
            removeSymbols = re.sub('([^A-Za-z0-9])+|(\d)|\s+', ' ', string,flags=re.UNICODE)
            #removeSymbols = re.sub('([^A-Za-z0-9]+)|(\d)|{\s+}', ' ', string)
            removeSymbols = " ".join(re.split("\s+", removeSymbols, flags=re.UNICODE))
            removeSymbols.strip()

            proxeirhlista.append(removeSymbols)

        ##Remove words under 3 characters
        words = [x for x in proxeirhlista if len(x) > 3]

        for i in words:
            if i in stop_words:
                pass
            else:
                wordToBeAdded = stemmer.stem(i)
                finalList.append(wordToBeAdded.encode('ascii','ignore'))

    return finalList

def searchForOtherOccurencies(strings,titles):
    # print strings
    df = 0
    pointerlist = {}
    invertedIndex = {}
    for key in titles:
        tf = 0
        for word in titles[key]:
            if word == strings:
                df += 1
                tf += 1
                pointerlist[key] = tf
            invertedIndex[strings] = pointerlist

    doc = open('myInvertedIndex.txt').read()

    if strings in doc:
        print "Yes there is a string"
    else:
        with open('myInvertedIndex.txt',"a") as myfile:
            print "New word added to invertedIndex"
            myfile.write(json.dumps(invertedIndex))
            myfile.write('\n')
            myfile.close()



def create_inv_index(bodies, titles):
    """Create a single inverted index for the dictionaries provided. Treat
    all keywords as if they come from the same field. In the inverted index
    retail document and term frequencies per the form below.
    Arguments:
        bodies: A dictionary of the form {doc_id: [terms]} for the terms found
        in the body (.W) of a document
        titles: A dictionary of the form {doc_id: [terms]} for the terms found
        in the title (.T) of a document
    Return:
        index: a dictionary {docId: [df, postings]}, where postings is a
        dictionary {docId: tf}.
        E.g. {'word': [3, {4: 2, 7: 1, 9: 3}]}
               ^       ^   ^        ^
               term    df  docid    tf
    """
    # Create a joint dictionary with pre-processed terms

    for i in titles:
        for string in titles[i]:
            searchForOtherOccurencies(string,titles)
    for key in bodies:
        for string in bodies[key]:
            searchForOtherOccurencies(string,bodies)



def load_inv_index(filename=INDEX_FILE):
    """Load an inverted index from the disk. The index is assummed to be stored
    in a text file with one line per keyword. Each line is expected to be
    `eval`ed into a dictionary of the form created by create_inv_index().

    Arguments:
        filename: the path of the inverted index file
    Return:
        a dictionary containing all keyworks and their posting dictionaries
    """


def write_inv_index(inv_index, outfile=INDEX_FILE):
    """Write the given inverted index in a file.
    Arguments:
        inv_index: an inverted index of the form {'term': [df, {doc_id: tf}]}
        outfile: (str) the path to the file to be created
    """


def eval_conj(inv_index, terms):
    """Evaluate the conjunction given in list of terms. In other words, the
    list of terms represent the query `term1 AND term2 AND ...`
    The documents satisfying this query will have to contain ALL terms.
    Arguments:
        inv_index: an inverted index
        terms: a list of terms of the form [str]
    Return:
        a set of (docId, score) tuples -- You can ignore `score` by
        substituting it with None
    """
    # Get the posting "lists" for each of the ANDed terms:
    
    # Basic AND - find the documents all terms appear in, setting scores to
    # None (set scores to tf.idf for ranked retrieval):


def eval_disj(conj_results):
    """Evaluate the conjunction results provided, essentially ORing the
    document IDs they contain. In other words the resulting list will have to
    contain all unique document IDs found in the partial result lists.
    Arguments:
        conj_results: results as they return from `eval_conj()`, i.e. of the
        form {(doc_id, score)}, where score can be None for non-ranked
        retrieval. 
    Return:
        a set of (docId, score) tuples - You can ignore `score` by substituting
        it with None
    """
    # Basic boolean - no scores, max(tf.idf) for ranked retrieval:


def main():
    """Load or create an inverted index. Parse user queries from stdin
    where words on each line are ANDed, while whole lines between them are
    ORed. Match the user query to the Cranfield collection and output matching
    documents as "ID: title", each on its own line, on stdout.
    """

    # If an index file exists load it; otherwise create a new inverted index
    # and write it into a file (you can use the variable INDEX_FILE):


    # Get and evaluate user queries from stdin. Terms on each line should be
    # ANDed, while results between lines should be ORed.
    # The output should be a space-separated list of document IDs. In the case
    # of unranked boolean retrieval they should be sorted by document ID, in
    # the case of ranked solutions they should be reverse-sorted by score
    # (documents with higher scores should appear before documents with lower
    # scores):

    parsed = parse_documents()
    titles = {}
    bodies = {}
    for key in parsed[1]:
        titles[key] = pre_process(parsed[1][key])
    for key in parsed[0]:
        bodies[key] = pre_process(parsed[0][key])

    #create_inv_index(bodies,titles)

if __name__ == '__main__':
    main()
