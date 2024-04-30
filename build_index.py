import sys
from indexer.index_utils import build_index_builder, build_index_from_index_builder, valid_index_builder, valid_index
from documents import check_if_0_documents, get_corpus_filename_from_prefix
from cli import get_prefixes_for_index_build

# check if given prefixes match existing corpuses
def check_valid_corpuses(trained_corpus_filename_prefix, search_corpus_filename_prefix):
    
    trained_corpus_filename = get_corpus_filename_from_prefix(trained_corpus_filename_prefix)
    if check_if_0_documents(trained_corpus_filename):
        print("sorry, invalid training corpus, try another one!")
        return False
    
    search_corpus_filename = get_corpus_filename_from_prefix(search_corpus_filename_prefix)
    if check_if_0_documents(search_corpus_filename):
        print("sorry, invalid search corpus, try another one!")
        return False
    
    return True

def build_if_missing_index(trained_corpus_filename_prefix, search_corpus_filename_prefix):
    
    valid_corpuses = check_valid_corpuses(trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    if not valid_corpuses:
        return False
    
    if not valid_index_builder(trained_corpus_filename_prefix):
        print("building new index builder from training corpus with prefix '" + trained_corpus_filename_prefix + "'")
        build_index_builder(trained_corpus_filename_prefix)
        
        print(
            "building new index using index builder trained on corpus with prefix '" + 
            trained_corpus_filename_prefix + "'" +
            " on search corpus with prefix '" + search_corpus_filename_prefix + "'"
        )
        build_index_from_index_builder(trained_corpus_filename_prefix, search_corpus_filename_prefix)
        return True
    
    elif not valid_index(trained_corpus_filename_prefix, search_corpus_filename_prefix):
        print(
            "building new index using index builder trained on corpus with prefix '" + 
            trained_corpus_filename_prefix + "'" +
            " on search corpus with prefix '" + search_corpus_filename_prefix + "'"
        )
        build_index_from_index_builder(trained_corpus_filename_prefix, search_corpus_filename_prefix)
        return True
    else:
        print("nothing to build.")
        return True

def overwrite_build_index(trained_corpus_filename_prefix, search_corpus_filename_prefix):
    
    valid_corpuses = check_valid_corpuses(trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    if not valid_corpuses:
        return False
    
    if valid_index_builder(trained_corpus_filename_prefix):
        print("rebuilding index builder from training corpus with prefix '" + trained_corpus_filename_prefix + "'")
    else:
        print("building new index builder from training corpus with prefix '" + trained_corpus_filename_prefix + "'")
    
    build_index_builder(trained_corpus_filename_prefix)
    
    if valid_index(trained_corpus_filename_prefix, search_corpus_filename_prefix):
        print(
            "rebuilding index using index builder trained on corpus with prefix '" + 
            trained_corpus_filename_prefix + "'" +
            " on search corpus with prefix '" + search_corpus_filename_prefix + "'"
        )
    else:
        print(
            "building new index using index builder trained on corpus with prefix '" + 
            trained_corpus_filename_prefix + "'" +
            " on search corpus with prefix '" + search_corpus_filename_prefix + "'"
        )
        
    build_index_from_index_builder(trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    return True


if __name__ == "__main__":
    
    prms = get_prefixes_for_index_build(sys.argv[1:])
    if prms is not None:
        success = overwrite_build_index(*prms)
        if success:
            print("build successful!")
        else:
            print("build unsuccessful.")