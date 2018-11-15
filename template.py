
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re

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
    openedDocument = open(cran_file,'r')
    count = 0

    line = openedDocument.readlines()
    cnt = 1
    # wordsLists= []


    documentDict = {}
    bookDict = {}
    titleDict = {}
    for i in range(0,len(line)):

        wordsOfTitles = []
        listOfBooks = []
        lines = line[i]
        # print(lines)
        if '.I' in lines:
            global id
            id = line[i]
            match = re.match(r'.I (.*)',id,re.I|re.M)
            if match:
                id = id.replace(id,match.group(1))
                id = int(id)
                #print(id)

        if '.T' in lines:
            if '.A' in line[i+1]:
                print("Title not found")
            else:
                title = line[i + 1]
                wordsOfTitles.append(title)
            titleDict[id] = wordsOfTitles
        if '.B' in lines:
            if '.W' in line[i+1]:
                print("Book not found")

            else:
                book = line[i + 1]

        if '.A' in lines:
            if '.B' in line[i+1]:
                print("Author not found")

            else:
                author = line[i + 1]

        if '.W' in lines:
            otherLines = []
            sum = 0
            try:
                wordsLists = []
                #while '.I' not in line[i+1]:

                while '.I' not in line[i+1]: #line[i+1]:
                    sum+= 1
                    wordsInAbook = line[i+1]
                    #wordsInAbook = re.split(r"[-()\"#/@;:<>{}`+=~|.!?,]",'',wordsInAbook)
                    wordsLists.append(wordsInAbook)
                    i += 1
                listOfBooks.append(wordsLists)
                bookDict[id] = listOfBooks
                #documentDict[id] = listOfBooks
                del listOfBooks
                del wordsLists

                #print('----------')
            except IndexError:
               print("End of File...")

        del wordsOfTitles
    #print titleDict
    return bookDict,titleDict

def other_process(listaki):
    stemmer = PorterStemmer()

    otherList = []

    for string in listaki:
        #print string
        a = re.sub(r'\n', "", string)
        commas = re.sub(r',', '', a)
        apostrofos = re.sub(r"'", "", commas)

        hmiparenthesis = re.sub(r'\(', "", apostrofos)
        otherhmiparenthesis = re.sub(r'\)', "", hmiparenthesis)
        y = re.sub(r'\s +', '', otherhmiparenthesis)
        g = re.sub(r'\b\w{1,3}\b', '', y)
        w = re.sub(r'-', ' ', g)

        removeDot = re.sub(r'\.', '', w)
        bigspace = re.sub(r'    ', '', removeDot)
        minispace = re.sub(r'   ', ' ', bigspace)
        space = re.sub(r'  ', ' ', minispace)
        newStemmed = stemmer.stem(space)
        newStemmed.join(listaki)

        #newStemmed.join(listaki)
    #print listaki
    #print otherList

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
    titleAfterRemovedSymbolAndLengthList = []
    newlist = []
    preProcessedBookList = []
    newDiction = {}
    otherList = []

    # for key in range(1,len(words)):
    j = 0
    for value in words:
        for sublist in words[value]:
            hahalist = []
            if type(sublist) is list:
                if j == 0:
                    other_process(sublist)
                    j =1

            #split = re.split(r'[`=~!.@#$%^&*()_+\[\]-{};\'\\:"|<,./<>?]',sublist)
            # sublist = re.split('',sublist)
            #
            # for chrs in sublist:
            #     #remove \n
            #
            #     x = re.sub(r'\n','',chrs)
            #     commas = re.sub(r',','',x)
            #     apostrofos = re.sub(r"'","",commas)
            #     y = re.sub(r'\s +','',apostrofos)
            #     g = re.sub(r'\b\w{1,3}\b','',y)
            #     w = re.sub(r'-',' ',g)
            #
            #     removeDot = re.sub(r'\.','',w)
            #     bigspace = re.sub(r'    ','',removeDot)
            #     minispace = re.sub(r'   ',' ',bigspace)
            #     space = re.sub(r'  ',' ',minispace)
            #
            #     stemmed = stemmer.stem(space)
            #
            #     words[value] = stemmed



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
    #pre_process(parsed[0])

if __name__ == '__main__':
    main()