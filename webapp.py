import sys
from pathlib import Path

path = str(Path(__file__).parent.parent)
sys.path.insert(1, path)

from cli import get_run_cli_build
from processor.query_processor import get_top_k_inds_by_score
from documents import load_document

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for

import logging

import webbrowser
from threading import Timer

home_filename = "index"
home_routename = "index"
view_results_filename = "view_results"

view_results_routename = "view_results"
enter_query_routename = "enter_query"

# open browser in new tab, start webapp
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8080")

# set app config with data filenames for corpus and index
def set_app_data(app, corpus_filename, index_filename):
    app.config["corpus_filename"] = corpus_filename
    app.config["index_filename"] = index_filename
    
# given query string and number of results k
# - process query and compile list of results to display
# return result comment text and list of results to display
def get_results(app, query_str, k):
    result_comment = ""
    results = []
    
    if k > 0:
        # get results from query processor
        top_k_inds_by_score = get_top_k_inds_by_score(app.config["index_filename"], query_str, k)
        
        if top_k_inds_by_score is None: # invalid query
            result_comment = "Sorry, invalid query could not be searched. Try again!"
        else:
            # get results from corpus file
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
    else:
        result_comment = "Sorry, invalid number of results. Try again!"
        
    return {
        "result_comment": result_comment,
        "results": results
    }

# return search webapp app 
def create_app():
    app = Flask(__name__)

    # page with empty search bar and default k
    @app.route("/")
    @app.route("/" + home_routename)
    # @app.route("/" + home_filename + ".html")
    def index():
        return render_template(home_filename + ".html")
        
    # page for entering query
    # - get query form POST json data and go to `view results` page
    @app.route("/" + enter_query_routename, methods = ["POST", "GET"])
    def enter_query():
        if request.method == "POST":
            query_str = request.form["query"]
            k = request.form["k_value"]
            try: 
                k = int(k)
                valid_k = k > 0
            except ValueError:
                return view_results(query_str, -1)
                
            if valid_k:
                return redirect(url_for(view_results_routename, query_str=query_str, k=k))
            else:
                return view_results(query_str, k)
                
        else:
            return redirect(request.referrer)
        
    
    # given query string and number of results k (may come from url route)
    # - get results from query processor
    # page for viewing results
    @app.route("/" + view_results_routename + "/<query_str>/<int:k>")
    def view_results(query_str, k):
        
        res = get_results(app, query_str, k)
        
        return render_template(
            view_results_filename + ".html", 
            result_comment=res["result_comment"],
            query=query_str,
            k_value=k,
            results=res["results"]
        )
        
    # page with empty search bar and user-entered k (from url route)
    @app.route("/" + view_results_routename + "//<int:k>")
    def empty_query(k):
        return render_template(
            view_results_filename + ".html", 
            result_comment="",
            query="",
            k_value=k,
            results=[]
        )

    return app


if __name__ == "__main__":
    
    # get specific corpus and index from cli arguments
    # and run search webapp on corpus and index
    
    build = get_run_cli_build(sys.argv)
    if build is not None:
        (corpus_filename, index_filename) = build
        
        app = create_app()
        set_app_data(app, corpus_filename, index_filename)
        
        Timer(1, open_browser).start()
        logging.getLogger('werkzeug').disabled = True
        app.run(
            host='0.0.0.0', 
            port=8080, 
            # debug = True, 
            use_reloader=False
        )
            
            