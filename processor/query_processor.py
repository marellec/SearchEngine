import numpy as np
from indexer.index_utils import load_inverted_index
from sklearn.metrics.pairwise import linear_kernel

# given filename for index, query string, and number of results k
# - process query and search index
# return top k document indices (in order of cosine similarity, high to low)
def get_top_k_inds_by_score(index_filename, query_str, k=5):
    
    if query_str.strip() == "": # empty query
        return None
    
    (vectorizer, doc_vectors) = load_inverted_index(index_filename)
    
    if k > doc_vectors.shape[0]: # requested more results than documents
        k = doc_vectors.shape[0]

    query_vector = vectorizer.transform([query_str])
    
    if query_vector.nnz == 0: # no terms in query that are in vocabulary
        return []

    #####   STOLEN FROM https://stackoverflow.com/questions/68003003/python-sklearn-tfidfvectorizer-vectorize-documents-ahead-of-query-for-semantic

    # REPLACE THIS ! ! ! ! !

    # compute cosine similarity between query and doc vector for each doc in corpus
    cosine_similarities = linear_kernel(doc_vectors, query_vector).flatten()

    # get top k document indices (in order of cosine similarity, high to low)
    doc_inds_by_score_reversed = np.argsort(cosine_similarities)
    top_k_inds_by_score_reversed = doc_inds_by_score_reversed[len(doc_inds_by_score_reversed)-k:]
    top_k_inds_by_score = top_k_inds_by_score_reversed[::-1]
    
    return top_k_inds_by_score
    

    
