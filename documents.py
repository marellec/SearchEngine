import os
import linecache
import json
from pathlib import Path

# get filename given filename prefix
def create_prefix_filename(filename_prefix, filename):
    return filename_prefix + "_" + filename

# get filename for corpus given filename prefix
def get_corpus_filename_from_prefix(corpus_filename_prefix):
    filename = "items.jsonl"
    filename = create_prefix_filename(corpus_filename_prefix, filename)
    return filename

# construct filepath from corpus filename
def get_corpus_filepath(corpus_filename):
    return str(
        Path(__file__)
        .with_name("corpus")
        .joinpath(corpus_filename)
    )

# check if there were no documents downloaded to file
def check_if_0_documents(corpus_filename):
    corpus_filepath = get_corpus_filepath(corpus_filename)
    is_file = os.path.exists(corpus_filepath)
    if is_file:
        with open(corpus_filepath, "r") as f:
            for i, _ in enumerate(f):
                if i >= 0:
                    return False
            return True
    else:
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
    
# get single `json document : dict["url" : str, "text" : str]` from file by index (given filename for corpus)
def load_document(corpus_filename, index):
    line = linecache.getline(get_corpus_filepath(corpus_filename), index+1)
    doc = json.loads(line)
    return doc

# transer documents from source corpus file to corpus file from start index for num_docs documents
def transer_documents(source_corpus_filename, corpus_filename, start_index, num_docs):
    with (
        open(get_corpus_filepath(source_corpus_filename), "r") as source_f,
        open(get_corpus_filepath(corpus_filename), "w") as f
    ):
        stop_index = start_index + num_docs
        for i, doc_str in enumerate(source_f.readlines()):
            if start_index <= i < stop_index:
                f.write(doc_str)
