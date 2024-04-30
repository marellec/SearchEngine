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


# app fixture
@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    
    yield app

# client fixture
@pytest.fixture()
def client(app):
    return app.test_client()






# return url with spaces replaced with "%20"
def url_spaces(url):
    return re.sub(" ", "%20", url)




# queries tested for search functionality and result quality
class TestSampleSet:

    def test_query_one(self, app):
        
        """
            90 training docs
            10 test docs
        """
        
        trained_corpus_filename_prefix = "big_whale_train"
        search_corpus_filename_prefix = "small_whale_test"
        set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
        
        
        query_str = "people in Africa"
        k = 5
        
        res = get_results(app, query_str, k)
        
    def test_query_two(self, app):
        
        """
            90 training docs
            10 test docs
        """
        
        trained_corpus_filename_prefix = "big_whale_train"
        search_corpus_filename_prefix = "small_whale_test"
        set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
        
        
        query_str = "fish"
        k = 5
        
        res = get_results(app, query_str, k)
        
    def test_query_three(self, app):
        
        """
            90 training docs
            10 test docs
        """
        
        trained_corpus_filename_prefix = "big_whale_train"
        search_corpus_filename_prefix = "small_whale_test"
        set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
        
        
        query_str = "animal"
        k = 5
        
        res = get_results(app, query_str, k)


# test processing a valid query with different k values
def test_valid_query(app):
    
    """
        10 docs
    """
    
    trained_corpus_filename_prefix = "small_test"
    search_corpus_filename_prefix = trained_corpus_filename_prefix
    set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    
    query_str = "written language"
    k = 2
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == ""
    assert len(results) == k
    
    k = 3
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == ""
    assert len(results) == k

# test processing a valid query with k that exceeds results found
def test_valid_query_k_over(app):
    
    """
        10 docs
    """
    
    trained_corpus_filename_prefix = "small_test"
    search_corpus_filename_prefix = trained_corpus_filename_prefix
    set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    
    query_str = "written language"
    k = 5
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == "Less than k=5 results found. Showing 3 results."
    assert len(results) == 3

# test processing a valid query that has no results
def test_valid_query_no_results(app):
    
    """
        10 docs
    """
    
    trained_corpus_filename_prefix = "small_test"
    search_corpus_filename_prefix = trained_corpus_filename_prefix
    set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    
    query_str = "hi"
    k = 5
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == "Sorry, no results found. Try another query!"
    assert len(results) == 0

# test processing an invalid (empty) query
def test_invalid_query(app):
    
    """
        10 docs
    """
    
    trained_corpus_filename_prefix = "small_test"
    search_corpus_filename_prefix = trained_corpus_filename_prefix
    set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    
    query_str = ""
    k = 5
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == "Sorry, invalid query could not be searched. Try again!"
    assert len(results) == 0

# test processing an invalid (negative) k
def test_invalid_k(app):
    
    """
        10 docs
    """
    
    trained_corpus_filename_prefix = "small_test"
    search_corpus_filename_prefix = trained_corpus_filename_prefix
    set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    
    query_str = "written language"
    k = -5
    
    res = get_results(app, query_str, k)
    
    result_comment = res["result_comment"]
    results = res["results"]
    
    assert result_comment == "Sorry, invalid number of results. Try again!"
    assert len(results) == 0
 
    
# test that when user enters a query with valid k,
# results page is displayed
def test_enter_valid_k(app, client):
    
    """
        10 docs
    """
    
    trained_corpus_filename_prefix = "small_test"
    search_corpus_filename_prefix = trained_corpus_filename_prefix
    set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    
    query_str = "written language"
    k = 4
    
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

# test that when user enters a query with invalid (negative) k,
# user is redirected to page to re-enter k
def test_enter_invalid_k_negative(app, client):
    
    """
        10 docs
    """
    
    trained_corpus_filename_prefix = "small_test"
    search_corpus_filename_prefix = trained_corpus_filename_prefix
    set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    
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

# test that when user enters a query with invalid (non-integer) k,
# user is redirected to page to re-enter k
def test_enter_invalid_k_not_int(app, client):
    
    """
        10 docs
    """
    
    trained_corpus_filename_prefix = "small_test"
    search_corpus_filename_prefix = trained_corpus_filename_prefix
    set_app_data(app, trained_corpus_filename_prefix, search_corpus_filename_prefix)
    
    
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
