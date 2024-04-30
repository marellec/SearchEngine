import numpy as np
from indexer.index_utils import load_index_builder, load_index
from sklearn.metrics.pairwise import linear_kernel

# given given trained corpus filename prefix, search corpus filename prefix, query string, and number of results k
# - process query and search index
# return top k document indices (in order of cosine similarity, high to low)
def get_top_k_inds_by_score(trained_corpus_filename_prefix, search_corpus_filename_prefix, query_str, k=5):
    
    # similarity score must be above threshold
    threshold = 0.02
    
    if query_str.strip() == "": # empty query
        return None
    
    (doc_vectorizer, query_vectorizer) = load_index_builder(trained_corpus_filename_prefix)
    doc_vectors = load_index(trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    if k > doc_vectors.shape[0]: # requested more results than documents
        k = doc_vectors.shape[0]

    query_vector = query_vectorizer.transform([query_str])
    
    if query_vector.nnz == 0: # no terms in query that are in vocabulary
        return []
    
    ####    https://stackoverflow.com/questions/68003003/python-sklearn-tfidfvectorizer-vectorize-documents-ahead-of-query-for-semantic

    # compute cosine similarity between query and doc vector for each doc in corpus
    cosine_similarities = linear_kernel(doc_vectors, query_vector).flatten()

    # get top k document indices (in order of cosine similarity, high to low)
    doc_inds_by_score_reversed = np.argsort(cosine_similarities)
    top_k_inds_by_score_reversed = doc_inds_by_score_reversed[len(doc_inds_by_score_reversed)-k:]
    top_k_inds_by_score = top_k_inds_by_score_reversed[::-1]
    # get rid of scores below threshold
    top_k_inds_by_score = [i for i in top_k_inds_by_score if cosine_similarities[i] > threshold]
    
    return top_k_inds_by_score
    

    
