import re
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import pickle
from documents import load_documents_text


def temp_tokenizer(text: str) -> list[str]:
    toks = re.split(r"\s", text)
    toks = [
        s for s in toks 
        # filter out empty tokens
        if len(s) > 0
    ]
    return toks

def temp_preprocessor(text: str) -> str:
    text = text.strip()
    # remove everything except letters, numbers, and '-'
    text = re.sub(r'[^a-zA-Z0-9\-\s]', ' ', text) 
    # apply lowercasing
    text = text.lower() 
    # remove non-ascii chars
    text = "".join(ch for ch in text if ord(ch) <= 127) 
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

def build_inverted_index(corpus_filename, index_filename):
    
    documents = load_documents_text(corpus_filename)
    
    vectorizer = TfidfVectorizer(
        preprocessor=temp_preprocessor, 
        tokenizer=temp_tokenizer,
        token_pattern=None
    )

    doc_vectors = vectorizer.fit_transform(documents)
    
    save_inverted_index(index_filename, (vectorizer, doc_vectors))
    
    