import nltk
import sys
import os
import string
import math
import operator
from collections import OrderedDict
import ssl


# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('stopwords')
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    mapped_files = {}
    for root, subdirectories, files in os.walk(directory):
        for file in files:
            if "." in file:
                file_name, file_extension = file.split(".")
            else:
                continue
            if file_extension == "txt":
                f = open(os.path.join(root, file), "r")
                mapped_files[file_name] = f.read()
    return mapped_files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = []
    tokens.extend([
        word.lower() for word in
        nltk.word_tokenize(document)
        if any(c.isalpha() for c in word) and
        word not in string.punctuation and
        word not in nltk.corpus.stopwords.words("english")
    ])
    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    words = set()
    for filename in documents:
        words.update(documents[filename])
    idfs = dict()
    for word in words:
        f = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranking = {}
    for file in files:
        for word in query:
            tf_ids_sum = 0
            if word in files[file]:
                tf_ids_sum += idfs[word]
        ranking[file] = tf_ids_sum

    # sort dictionary
    # source: https://stackoverflow.com/questions/40777570/get-n-largest-key-value-in-a-dictionary
    sorted_ranking = {key: ranking[key] for key in sorted(ranking, key=ranking.get, reverse=True)}

    return list(sorted_ranking.keys())[:n]


def dict_sort_compare(x, y):
    print(x, y)
    return x - y


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranking = {}
    for sentence in sentences:
        for word in query:
            tf_ids_sum = 0
            if word in sentences[sentence]:
                tf_ids_sum += idfs[word]
        ranking[sentence] = tf_ids_sum

    sorted_ranking = {key: ranking[key] for key in sorted(ranking, cmp=dict_sort_compare, reverse=True)}

    return list(sorted_ranking.keys())[:n]


if __name__ == "__main__":
    main()
