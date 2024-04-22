import pytest

import re

from flask import url_for

from webapp import (
    create_app, 
    set_app_data,
    
    get_results,
    
    home_filename,
    home_routename,
    view_results_filename,

    view_results_routename,
    enter_query_routename
)
from documents import get_build_from_prefix, get_build_from_prefixes

@pytest.fixture()
def app():
    
    corpus_filename = "items.jsonl"
    index_filename = "index.pkl"
    
    app = create_app(corpus_filename, index_filename)
    app.config.update({
        "TESTING": True,
    })
    
    yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()





def set_app_data_from_prefix(app, save_filename_prefix):
    (corpus_filename, index_filename) = get_build_from_prefix(save_filename_prefix)
    set_app_data(app, corpus_filename, index_filename)
    

    
def set_app_data_from_prefixes(app, save_filename_prefix1, save_filename_prefix2):
    (corpus_filename, index_filename) = get_build_from_prefixes(save_filename_prefix1, save_filename_prefix2)
    set_app_data(app, corpus_filename, index_filename)


def url_spaces(url):
    return re.sub(" ", "%20", url)





class TestSampleSet:

    def test_query_one(self, app):
        
        """
            100 docs
        """
        
        save_filename_prefix = "one_test"
        set_app_data_from_prefix(app, save_filename_prefix)
        
        
        query_str = "uhh"
        k = 5
        
        res = get_results(app, query_str, k)
        
        result_comment = res["result_comment"]
        results = res["results"]
        
        
        
    def test_query_one(self, app):
        
        """
            100 docs
        """
        
        save_filename_prefix = "one_test"
        set_app_data_from_prefix(app, save_filename_prefix)
        
        
        query_str = "uhh"
        k = 5
        
        res = get_results(app, query_str, k)
        
        result_comment = res["result_comment"]
        results = res["results"]
        
        
        
        
        











def test_valid_query(app):
    
    """
        10 docs
    """
    
    save_filename_prefix = "small_test"
    set_app_data_from_prefix(app, save_filename_prefix)
    
    
    query_str = "written language"
    k = 5
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == ""
    assert len(results) == k

def test_valid_query_k_over(app):
    
    """
        10 docs
    """
    
    save_filename_prefix = "small_test"
    set_app_data_from_prefix(app, save_filename_prefix)
    
    
    query_str = "written language"
    k = 11
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == "Less than k=11 results found. Showing 10 results."
    assert len(results) == 10

def test_valid_query_no_results(app):
    
    """
        10 docs
    """
    
    save_filename_prefix = "small_test"
    set_app_data_from_prefix(app, save_filename_prefix)
    
    
    query_str = "hi"
    k = 5
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == "Sorry, no results found. Try another query!"
    assert len(results) == 0
    
def test_invalid_query(app):
    
    """
        10 docs
    """
    
    save_filename_prefix = "small_test"
    set_app_data_from_prefix(app, save_filename_prefix)
    
    
    query_str = ""
    k = 5
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == "Sorry, invalid query could not be searched. Try again!"
    assert len(results) == 0
    
def test_invalid_k(app):
    
    """
        10 docs
    """
    
    save_filename_prefix = "small_test"
    set_app_data_from_prefix(app, save_filename_prefix)
    
    
    query_str = "written language"
    k = -5
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == "Sorry, invalid number of results. Try again!"
    assert len(results) == 0
 
    
    
def test_enter_valid_k(app, client):
    
    """
        10 docs
    """
    
    save_filename_prefix = "small_test"
    set_app_data_from_prefix(app, save_filename_prefix)
    
    
    query_str = "written language"
    k = 5
    
    with app.app_context(), app.test_request_context():
        response = client.post(
            "/enter_query", data={
                "query": query_str,
                "k_value": k
            }, 
            follow_redirects=True
        )
        
        assert response.status_code == 200
    
        assert (
            url_spaces(response.request.path) == 
            url_for(view_results_routename, query_str=query_str, k=k)
        )
        
def test_enter_invalid_k_negative(app, client):
    
    """
        10 docs
    """
    
    save_filename_prefix = "small_test"
    set_app_data_from_prefix(app, save_filename_prefix)
    
    
    query_str = "written language"
    k = -5
    
    with app.app_context(), app.test_request_context():
        response = client.post(
            "/enter_query", data={
                "query": query_str,
                "k_value": k
            }, 
            follow_redirects=True
        )
        
        assert response.status_code == 200
    
        assert (
            url_spaces(response.request.path) == 
            url_for(enter_query_routename)
        )
        
def test_enter_invalid_k_not_int(app, client):
    
    """
        10 docs
    """
    
    save_filename_prefix = "small_test"
    set_app_data_from_prefix(app, save_filename_prefix)
    
    
    query_str = "written language"
    k = "hi"
    
    with app.app_context(), app.test_request_context():
        response = client.post(
            "/enter_query", data={
                "query": query_str,
                "k_value": k
            }, 
            follow_redirects=True
        )
        
        assert response.status_code == 200
    
        assert (
            url_spaces(response.request.path) == 
            url_for(enter_query_routename)
        )
        

def test_enter_valid_query(app, client):
    
    """
        10 docs
    """
    
    save_filename_prefix = "small_test"
    set_app_data_from_prefix(app, save_filename_prefix)
    
    
    query_str = "written language"
    k = 5
    
    with app.app_context(), app.test_request_context():
        response = client.get(
            url_for(view_results_routename, query_str=query_str, k=k),
            follow_redirects=True
        )

        assert response.status_code == 200
        
        
    





# class TestClass1:
#     value = 0

#     def test_one(self):
#         self.value = 1
#         assert self.value == 1

#     # def test_two(self):
#     #     assert self.value == 1