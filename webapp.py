import sys
from pathlib import Path

path = str(Path(__file__).parent.parent)
sys.path.insert(1, path)

from cli import get_cli_options
from build import build_search_engine
from processor.query_processor import get_top_k_inds_by_score
from documents import load_document

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for

import logging

import webbrowser
from threading import Timer

app = Flask(__name__)

# template_folder_prefix = "templates/"
home_filename = "index"
home_routename = "index"
view_results_filename = "view_results"

view_results_routename = "view_results"
enter_query_routename = "enter_query"

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8080")

@app.route("/")
@app.route("/" + home_routename)
# @app.route("/" + home_filename + ".html")
def index():
    return render_template(home_filename + ".html")
    
@app.route("/" + enter_query_routename, methods = ["POST", "GET"])
def enter_query():
    if request.method == "POST":
        query_str = request.form["query"]
        k = request.form["k_value"]
        return redirect(url_for(view_results_routename, query_str=query_str, k=k))
    else:
        return redirect(request.referrer)

@app.route("/" + view_results_routename + "/<query_str>/<int:k>")
def view_results(query_str, k):
    
    # get results from query processor
    top_k_inds_by_score = get_top_k_inds_by_score(app.config["index_filename"], query_str, k)
    
    result_comment = ""
    results = []
    
    if top_k_inds_by_score is None: # invalid query
        result_comment = "Sorry, invalid query could not be searched. Try again!"
    else:
        for n, i in enumerate(top_k_inds_by_score, 1):
            doc = load_document(app.config["corpus_filename"], i)
            results.append((n, doc["url"], doc["text"][:250] + "..."))
        
        if len(results) < k:
            result_comment = (
                "Sorry, no results found. Try another query!" 
                if len(results) == 0 else 
                (f"Less than k={k} results found. Showing " +
                str(len(results)) +
                " results.")
            )
    
    # results = [
    #     (1, url_for(home_routename), "this is result 1..." + query_str),
    #     (2, url_for(home_routename), "this is result 2..." + query_str),
    #     (3, url_for(home_routename), "this is result 3..." + query_str)
    # ]
    
    return render_template(
        view_results_filename + ".html", 
        result_comment=result_comment,
        query=query_str,
        k_value=k,
        results=results
    )
    
@app.route("/" + view_results_routename + "//<int:k>")
def empty_query(k):
    return render_template(
        view_results_filename + ".html", 
        result_comment="",
        query="",
        k_value=k,
        results=[]
    )



if __name__ == "__main__":
    
    options = get_cli_options(sys.argv)
    
    if options is not None:
        build = build_search_engine(*options)
        if build is not None:
            (corpus_filename, index_filename) = build
            app.config["corpus_filename"] = corpus_filename
            app.config["index_filename"] = index_filename
            
            Timer(1, open_browser).start()
            logging.getLogger('werkzeug').disabled = True
            app.run(
                host='0.0.0.0', 
                port=8080, 
                # debug = True, 
                use_reloader=False
            )
            
            