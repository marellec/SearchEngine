import sys
from indexer.index_utils import build_index_builder, build_index_from_index_builder, valid_index_builder, valid_index
from documents import check_if_0_documents, get_corpus_filename_from_prefix, number_of_documents, transer_documents
from cli import get_prefixes_for_split_corpus

def split_corpus(source_corpus_filename_prefix, document_count1, corpus_filename_prefix1, document_count2, corpus_filename_prefix2):
    
    source_corpus_filename = get_corpus_filename_from_prefix(source_corpus_filename_prefix)
    corpus_filename1 = get_corpus_filename_from_prefix(corpus_filename_prefix1)
    corpus_filename2 = get_corpus_filename_from_prefix(corpus_filename_prefix2)
    
    if check_if_0_documents(source_corpus_filename):
        print("sorry, invalid source corpus, try another one!")
        return False
    
    if document_count1 + document_count2 > number_of_documents(source_corpus_filename):
        print("sorry, not enough documents for document counts, try again!")
        return False
    
    transer_documents(source_corpus_filename, corpus_filename1, 0, document_count1)
    transer_documents(source_corpus_filename, corpus_filename2, document_count1, document_count2)
    
    return True
    
if __name__ == "__main__":
    
    prms = get_prefixes_for_split_corpus(sys.argv[1:])
    if prms is not None:
        success = split_corpus(*prms)
        if success:
            print("split successful!")
        else:
            print("split unsuccessful.")