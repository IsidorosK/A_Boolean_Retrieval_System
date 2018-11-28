#!/usr/bin/env python

#########################################################################
# Data Programming - MSc in Data Science 2018 - Assignment 1/2
# Author: KOUTSOUMPOS ISIDOROS
#########################################################################


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
    doc_dict = {}
    title_dict = {}

    global id
    for i in range(0,len(lines)):
        if lines[i].startswith('.I'):
            linesplit = lines[i].split()
            id = int(linesplit[1])

        titles_list = []
        if lines[i].startswith('.T') :
            while not lines[i+1].startswith('.A'):
                linesplit = lines[i+1].split('\n')
                titles = linesplit[0]
                titles_list.append(titles)
                title_dict[id] = titles_list
                i+=1
        del titles_list

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
                        doc_dict[id] = lista
                    del lista
                except IndexError:
                    pass
    document.close()
    return doc_dict,title_dict

def pre_process(words):
    """Preprocess the list of words provided.
    Arguments:
        words: (list of str) A list of words or terms
    Return:
        a shorter list of pre-processed words
    """
    # Get list of stop-words and instantiate a stemmer:
    print "Will do the pre_process of words now.."
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    final_list = []

    for i in words:
        strings_splitted_list = i.split()
        proxeirhlista = []

        for string in strings_splitted_list:
            #### Remove symbolsw
            remove_symbols = re.sub(r'(\W)|[!@#$%^&*()[]{};\':",.<>/?`~-_=+]',' ',string,flags=re.UNICODE)

            remove_symbols.strip()
            proxeirhlista.append(remove_symbols)
        ##Remove words under 3 characters
        words = [x for x in proxeirhlista if len(x) > 3]

        for i in words:
            if i in stop_words:
                pass
            else:
                word_to_be_added = stemmer.stem(i)
                final_list.append(word_to_be_added.encode('ascii','ignore'))
    #print final_list
    return final_list

def create_inverted_index(bodies, titles):
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
    print "Creating inverted index...."
    dict_inv = {}
    for docId in bodies:
        for string in bodies[docId]:
            if string in dict_inv:
                dict_inv[string][0] += 1
                if docId in dict_inv[string][1]:
                    dict_inv[string][1][docId] += 1
                else:
                    dict_inv[string][1][docId] = 1
            else:
                dict_inv[string] = [1,{docId:1}]
        for string in titles[docId]:
            if string in dict_inv:
                dict_inv[string][0] += 1
                if docId in dict_inv[string][1]:
                    dict_inv[string][1][docId] += 1
                else:
                    dict_inv[string][1][docId] = 1
            else:
                dict_inv[string] = [1,{docId:1}]

    return dict_inv


def load_inv_index(filename=INDEX_FILE):
    """Load an inverted index from the disk. The index is assummed to be stored
    in a text file with one line per keyword. Each line is expected to be
    `eval`ed into a dictionary of the form created by create_inv_index().

    Arguments:
        filename: the path of the inverted index file
    Return:
        a dictionary containing all keyworks and their posting dictionaries
    """
    try:
        inv_index = open(filename).readlines()
        inv_index = json.loads(inv_index[0])
    except IOError:
        print "Will create now the inverted index."
        parsed = parse_documents()
        titles = {}
        bodies = {}
        for key in parsed[1]:
            titles[key] = pre_process(parsed[1][key])
        for key in parsed[0]:
            bodies[key] = pre_process(parsed[0][key])
        inv_index = create_inverted_index(bodies, titles)
        write_inv_index(inv_index,INDEX_FILE)
    return inv_index

def write_inv_index(inv_index, outfile=INDEX_FILE):
    """Write the given inverted index in a file.
    Arguments:
        inv_index: an inverted index of the form {'term': [df, {doc_id: tf}]}
        outfile: (str) the path to the file to be created
    """
    with open(outfile,'w') as myfile:
        print "New word added to inverted index"
        #myfile.write(inv_index)
        myfile.write(json.dumps(inv_index))
        myfile.close()


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
    # Basic boolean - no scores, max(tf.idf) for ranked retrieval:\

def call_AND(inv_index, list_of_ANDs):
    inv = inv_index
    id_list = []
    list_of_ANDs_splitted = list_of_ANDs.split(' ')
    pre_processed_strings = pre_process(list_of_ANDs_splitted)

    for string in pre_processed_strings:
        if string in inv:
            id_list.append(list(inv[string][1].keys()))
    new_id_list = []
    and_list = []
    for sublists in id_list:
        for doc_id in sublists:
            if doc_id not in new_id_list:
                new_id_list.append(doc_id)
            else:
                and_list.append(doc_id)

    return new_id_list,and_list

def call_OR(and_results):
    or_list = []
    for elements in and_results:
        for ids in elements:
            if ids not in or_list:
                or_list.append(ids)
    return or_list


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

    inv_index = load_inv_index()
    # inv = json.loads(inv_index[0])
    line = raw_input("Give input: ")

    x = line.split('\\n')
    and_results = []
    new_id_list = []
    for sublist in x:
        results = call_AND(inv_index, sublist)

        new_id_list.append(results[0])
        and_results.append(results[1])

    or_results = call_OR(new_id_list)
    print "AND results:",and_results
    print "OR results:",or_results


if __name__ == '__main__':
    main()
