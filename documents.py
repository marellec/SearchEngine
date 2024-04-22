import linecache
import json
from pathlib import Path

def create_prefix_filename(save_filename_prefix, filename):
    return save_filename_prefix + "_" + filename

def get_build_from_prefix(save_filename_prefix):
    corpus_filename = "items.jsonl"
    index_filename = "index.pkl"
    
    if save_filename_prefix is not None:
        corpus_filename = create_prefix_filename(save_filename_prefix, corpus_filename)
        index_filename = create_prefix_filename(save_filename_prefix, index_filename)
    
    return (corpus_filename, index_filename)

def get_build_from_prefixes(save_filename_prefix1, save_filename_prefix2):
    corpus_filename = "items.jsonl"
    index_filename = "index.pkl"
    
    corpus_filename = create_prefix_filename(save_filename_prefix1, corpus_filename)
    index_filename = create_prefix_filename(save_filename_prefix2, index_filename)
    
    return (corpus_filename, index_filename)

# construct filepath from filename
def get_corpus_filepath(corpus_filename):
    return str(
        Path(__file__)
        .with_name("corpus")
        .joinpath(corpus_filename)
    )

# check if there were no documents downloaded to file
def check_if_0_documents(corpus_filename):
    with open(get_corpus_filepath(corpus_filename), "r") as f:
        for i, _ in enumerate(f):
            if i >= 1:
                return False
        return True
    
# get number of documents in file
def number_of_documents(corpus_filename):
    if check_if_0_documents(corpus_filename):
        return 0
    
    with open(get_corpus_filepath(corpus_filename), "r") as f:
        i = 0
        for _ in f: i += 1
        return i

# get list of doctuments' text : list[str] from file
def load_documents_text(corpus_filename):
    documents = []
    with open(get_corpus_filepath(corpus_filename), "r") as f:
        for doc_str in f.readlines():
            doc = json.loads(doc_str)
            documents.append(doc["text"])
        return documents
    
# get single doctument : dict["url" : str, "text" : str] 
# from file by index
def load_document(corpus_filename, index):
    line = linecache.getline(get_corpus_filepath(corpus_filename), index+1)
    doc = json.loads(line)
    return doc
