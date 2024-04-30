import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import pickle
from documents import load_documents_text, create_prefix_filename, get_corpus_filename_from_prefix
from scipy.sparse._csr import csr_matrix


# tokenize text
def tokenizer(text: str) -> list[str]:
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
def get_save_filepath_for_index_builder(index_builder_filename):
    return str(
        Path(__file__)
        .parent
        .with_name("index_builder")
        .joinpath(index_builder_filename)
    )
    
# construct filepath from folder
def get_save_filepath_folder_for_index(trained_corpus_filename_prefix):
    return str(
        Path(__file__)
        .parent
        .with_name("index")
        .joinpath(trained_corpus_filename_prefix)
    )

# construct filepath from folder and filename
def get_save_filepath_for_index(trained_corpus_filename_prefix, index_filename):
    return str(
        Path(__file__)
        .parent
        .with_name("index")
        .joinpath(trained_corpus_filename_prefix)
        .joinpath(index_filename)
    )
    
# get filename for index builder given trained corpus filename prefix
def get_trained_index_builder_filename_from_prefix(trained_corpus_filename_prefix):
    filename = "index_builder.pkl"
    filename = create_prefix_filename(trained_corpus_filename_prefix, filename)
    filename = filename
    return filename

# get filename for index given trained corpus filename prefix and search corpus filename prefix
def get_search_index_filename_from_prefix(search_corpus_filename_prefix):
    filename = "index.pkl"
    filename = create_prefix_filename(search_corpus_filename_prefix, filename)
    return filename

# save index builder (vectorizers) to pickle file
def save_index_builder(trained_corpus_filename_prefix, index_builder: tuple[TfidfVectorizer]):
    index_builder_filename = get_trained_index_builder_filename_from_prefix(trained_corpus_filename_prefix)
    with open(get_save_filepath_for_index_builder(index_builder_filename), 'wb') as f:
        pickle.dump(index_builder, f)

# save index (document vector matrix) to pickle file
def save_index(trained_corpus_filename_prefix, search_corpus_filename_prefix, index: csr_matrix):
    index_folder = get_save_filepath_folder_for_index(trained_corpus_filename_prefix)
    index_filename = get_search_index_filename_from_prefix(search_corpus_filename_prefix)
    
    if not os.path.exists(index_folder):
        os.makedirs(index_folder)
    
    with open(get_save_filepath_for_index(trained_corpus_filename_prefix, index_filename), 'wb') as f:
        pickle.dump(index, f)

# get index builder (vectorizers) from file given filename prefix
def load_index_builder(trained_corpus_filename_prefix) -> tuple[TfidfVectorizer]:
    index_builder_filename = get_trained_index_builder_filename_from_prefix(trained_corpus_filename_prefix)
    with open(get_save_filepath_for_index_builder(index_builder_filename), 'rb') as f:
        return pickle.load(f)
        
# get index (document vector matrix) from file given filename prefixes
def load_index(trained_corpus_filename_prefix, search_corpus_filename_prefix) -> csr_matrix:
    index_filename = get_search_index_filename_from_prefix(search_corpus_filename_prefix)
    with open(get_save_filepath_for_index(trained_corpus_filename_prefix, index_filename), 'rb') as f:
        return pickle.load(f)

# check if filename prefix for index matches a valid index builder
def valid_index_builder(trained_corpus_filename_prefix):
    index_builder_filename = get_trained_index_builder_filename_from_prefix(trained_corpus_filename_prefix)
    index_builder_filepath = get_save_filepath_for_index_builder(index_builder_filename)
    is_file = os.path.exists(index_builder_filepath)
    if is_file:
        try:
            index_builder = load_index_builder(trained_corpus_filename_prefix)
            return (type(index_builder) == tuple and
                    len(index_builder) == 2 and
                    type(index_builder[0]) == TfidfVectorizer and
                    type(index_builder[1]) == TfidfVectorizer)
        except EOFError:
            return False
    return False
    
# check if filename prefixes for index match a valid index
def valid_index(trained_corpus_filename_prefix, search_corpus_filename_prefix):
    index_folder = get_save_filepath_folder_for_index(trained_corpus_filename_prefix)
    index_filename = get_search_index_filename_from_prefix(search_corpus_filename_prefix)
    index_filepath = get_save_filepath_for_index(trained_corpus_filename_prefix, index_filename)
    is_folder = os.path.exists(index_folder)
    is_file = os.path.exists(index_filepath)
    if is_folder and is_file:
        try:
            index = load_index(trained_corpus_filename_prefix, search_corpus_filename_prefix)
            return (type(index) == csr_matrix)
        except EOFError:
            return False
    return False

# given trained corpus filename prefix
# - make index builder (vectorizer) to:
# - preprocess/tokenize training corpus 
# - and create vocabulary
# - and count document frequencies (lnc.ltc weighting)
# save index builder (vectorizer) to file
def build_index_builder(trained_corpus_filename_prefix):
    
    documents = load_documents_text(get_corpus_filename_from_prefix(trained_corpus_filename_prefix))
    
    # lnc document vectorizer
    doc_vectorizer = TfidfVectorizer(
        preprocessor=temp_preprocessor, 
        tokenizer=tokenizer,
        token_pattern=None,
        stop_words="english",
        sublinear_tf=True, # (l) logarithmic term frequency (1 + log(tf))
        use_idf=False, # (n) idf score document frequency
        norm="l2" # (c) cosine normalization
    )
    
    # ltc query vectorizer
    query_vectorizer = TfidfVectorizer(
        preprocessor=temp_preprocessor, 
        tokenizer=tokenizer,
        token_pattern=None,
        stop_words="english",
        sublinear_tf=True, # (l) logarithmic term frequency (1 + log(tf))
        use_idf=True, # (t) idf score document frequency
        norm="l2" # (c) cosine normalization
    )

    # create vocabulary and compute tf-idf scores for corpus 
    doc_vectorizer.fit_transform(documents)
    query_vectorizer.fit_transform(documents)
    
    save_index_builder(trained_corpus_filename_prefix, (doc_vectorizer, query_vectorizer))

# given trained corpus filename prefix and search corpus filename prefix
# - use index builder (vectorizers) with vocabulary and document frequencies to:
# - preprocess/tokenize search corpus 
# - and count term occurences and document frequencies 
# - and compute tf-idf scores
# - in an inverted index in term-document matrix form
# save index (document vector matrix) to file
def build_index_from_index_builder(trained_corpus_filename_prefix, search_corpus_filename_prefix):
    
    documents = load_documents_text(get_corpus_filename_from_prefix(search_corpus_filename_prefix))
    
    (doc_vectorizer, query_vectorizer) = load_index_builder(trained_corpus_filename_prefix)

    # create vocabulary and compute tf-idf scores for corpus
    doc_vectors = doc_vectorizer.transform(documents)
    
    save_index(trained_corpus_filename_prefix, search_corpus_filename_prefix, doc_vectors)
    
    