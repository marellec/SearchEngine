import os
from pathlib import Path

from download_corpus import download_corpus
from build_index import overwrite_build_index

from cli import get_scraping_parameters
from documents import check_if_0_documents, number_of_documents, get_corpus_filename_from_prefix
from indexer.index_utils import valid_index_builder, valid_index, load_index, get_trained_index_builder_filename_from_prefix, get_search_index_filename_from_prefix

class TestBuild:

    # assert scraping web for downloading corpus and building index work
    def test_build(self):
        
        # build
        
        start_url = 'https://en.wikipedia.org/wiki/List_of_common_misconceptions'
        max_pages = 30
        max_depth = 3
        
        args = [
            "build_test",
            start_url,
            str(max_pages),
            str(max_depth)
        ]
        
        trained_corpus_filename_prefix = "build_test"
        search_corpus_filename_prefix = "build_test"
        
        prms = get_scraping_parameters(args)
        
        # valid scraping parameters
        assert prms is not None
        
        # valid crawl
        assert download_corpus(*prms)
        
        # valid corpus prefixes
        assert overwrite_build_index(trained_corpus_filename_prefix, search_corpus_filename_prefix)
        
        search_corpus_filename = get_corpus_filename_from_prefix(search_corpus_filename_prefix)
        
        # not empty or missing corpus
        assert not check_if_0_documents(search_corpus_filename)
        
        # not invalid or missing index builder
        assert valid_index_builder(trained_corpus_filename_prefix)
        
        # not invalid or missing index
        assert valid_index(trained_corpus_filename_prefix, search_corpus_filename_prefix)
            
        num_docs = number_of_documents(search_corpus_filename)
            
        # make sure the lengths match max pages
        assert num_docs <= max_pages
            
        doc_vectors = load_index(trained_corpus_filename_prefix, search_corpus_filename_prefix)
        
        # correct matrix shape
        assert num_docs == doc_vectors.shape[0]
        
        # delete corpus, index builder, and index
        
        search_corpus_filepath = str(
            Path(__file__)
            .with_name("corpus")
            .joinpath(search_corpus_filename)
        )
        
        index_builder_filepath =  str(
            Path(__file__)
            .with_name("index_builder")
            .joinpath(get_trained_index_builder_filename_from_prefix(trained_corpus_filename_prefix))
        )
        
        index_folder_filepath =  str(
            Path(__file__)
            .with_name("index")
            .joinpath(trained_corpus_filename_prefix)
        )
        
        index_filepath =  str(
            Path(__file__)
            .with_name("index")
            .joinpath(trained_corpus_filename_prefix)
            .joinpath(get_search_index_filename_from_prefix(search_corpus_filename_prefix))
        )
        
        
        if os.path.exists(search_corpus_filepath):
            os.remove(search_corpus_filepath)
        
        if os.path.exists(index_builder_filepath):
            os.remove(index_builder_filepath)
        
        if os.path.exists(index_filepath):
            os.remove(index_filepath)
            
        if os.path.exists(index_folder_filepath):
            os.remove(index_folder_filepath)
            
        
  