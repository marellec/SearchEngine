import sys
import os
from pathlib import Path

import build

from build import build_search_engine
from cli import get_build_cli_options
from documents import check_if_0_documents, number_of_documents, load_document
from indexer.index_utils import valid_index, load_inverted_index

class TestBuild:

    def test_build(self):
        
        # build
        
        start_url = 'https://en.wikipedia.org/wiki/List_of_common_misconceptions'
        max_pages = 30
        max_depth = 3
        
        argv = [
            None,
            start_url,
            max_pages,
            max_depth,
            "build_test"
        ]
        
        options = get_build_cli_options(argv)
    
        assert options is not None
        
        build = build_search_engine(*options)
        
        assert build is not None
        
        (corpus_filename, index_filename) = build
        
        
        # not empty or missing corpus corpus
        assert not check_if_0_documents(corpus_filename)
        
        # not invalid or missing index 
        assert valid_index(index_filename)
            
        num_docs = number_of_documents(corpus_filename)
            
        # make sure the lengths match max pages
        assert num_docs <= max_pages
            
        (vectorizer, doc_vectors) = load_inverted_index(index_filename)
        
        # correct matrix shape
        assert num_docs == doc_vectors.shape[0]
        
        # delete corpus and index
        
        index_filepath =  str(
            Path(__file__)
            .with_name("index")
            .joinpath(index_filename)
        )
        
        corpus_filepath = str(
            Path(__file__)
            .with_name("corpus")
            .joinpath(corpus_filename)
        )
        
        if os.path.exists(index_filepath):
            os.remove(index_filepath)
            
        if os.path.exists(corpus_filepath):
            os.remove(corpus_filepath)
  