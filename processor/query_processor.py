import numpy as np
from indexer.index_utils import load_inverted_index
from sklearn.metrics.pairwise import linear_kernel


def get_top_k_inds_by_score(index_filename, query_str, k=5):
    
    if query_str.strip() == "": # empty query
        return None
    
    # print("query: ", query_str)
    
    (vectorizer, doc_vectors) = load_inverted_index(index_filename)

    query_vector = vectorizer.transform([query_str])
    
    # print("query_vector size: ", query_vector.nnz)
    
    if query_vector.nnz == 0: # no terms in query
        return []

    #####   STOLEN FROM https://stackoverflow.com/questions/68003003/python-sklearn-tfidfvectorizer-vectorize-documents-ahead-of-query-for-semantic

    # REPLACE THIS ! ! ! ! !

    cosine_similarities = linear_kernel(doc_vectors, query_vector).flatten()

    doc_inds_by_score_reversed = np.argsort(cosine_similarities)
    top_k_inds_by_score_reversed = doc_inds_by_score_reversed[len(doc_inds_by_score_reversed)-k:]
    top_k_inds_by_score = top_k_inds_by_score_reversed[::-1]
    
    return top_k_inds_by_score
    

    
