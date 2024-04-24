import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import pickle
from documents import load_documents_text
import scipy


# tokenize text
def temp_tokenizer(text: str) -> list[str]:
    toks = re.split(r"\s", text)
    toks = [
        s for s in toks 
        # filter out empty tokens
        if len(s) > 0
    ]
    return toks

# preprocess test
def temp_preprocessor(text: str) -> str:
    text = text.strip()
    # remove everything except letters, numbers, and '-'
    text = re.sub(r'[^a-zA-Z0-9\-\s]', ' ', text) 
    # apply lowercasing
    text = text.lower() 
    return text

# construct filepath from filename
def get_save_filepath(index_filename):
    return str(
        Path(__file__)
        .parent
        .with_name("index")
        .joinpath(index_filename)
    )

# save (vectorizer, doc_vectors) to pickle file
def save_inverted_index(index_filename, inverted_index):
    with open(get_save_filepath(index_filename), 'wb') as f:
        pickle.dump(inverted_index, f)
        
# get (vectorizer, doc_vectors) from file
def load_inverted_index(index_filename):
    with open(get_save_filepath(index_filename), 'rb') as f:
        return pickle.load(f)
    
# check if filename for index matches a valid index
def valid_index(index_filename):
    is_file = os.path.isfile(get_save_filepath(index_filename))
    if is_file:
        try:
            inverted_index = load_inverted_index(index_filename)
            return (
                type(inverted_index) == tuple and 
                len(inverted_index) == 2 and
                type(inverted_index[0]) == TfidfVectorizer and
                type(inverted_index[1]) == scipy.sparse._csr.csr_matrix
            )
        except EOFError:
            return False
    return False

# given filename for corpus and filename for index
# - use vectorizer to preprocess/tokenize corpus 
# - and create vocabulary
# - and count term occurences and document frequencies 
# - and compute tf-idf scores
# - in an inverted index in term-document matrix form
# save vectorizer and document vector matrix to index file
def build_inverted_index(corpus_filename, index_filename):
    
    documents = load_documents_text(corpus_filename)
    
    vectorizer = TfidfVectorizer(
        preprocessor=temp_preprocessor, 
        tokenizer=temp_tokenizer,
        token_pattern=None
    )

    # create vocabulary and compute tf-idf scores for corpus
    doc_vectors = vectorizer.fit_transform(documents)
    
    save_inverted_index(index_filename, (vectorizer, doc_vectors))
    
    