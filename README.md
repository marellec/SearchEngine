# Search Engine

This search engine aims to efficiently index and retrieve information from online content starting from anywhere on the web. The corpuses compiled from crawled pages will be indexed using the vector space model with weights that enhance query matching and ranking of results, so users can find what's relevant with ease. Potential improvements down the line would be restructuring the vector space with vector embeddings for terms. This would be implemented using the word2vec Skip Gram model that represents terms by their relationships with surrounding context words.

## Overview

The crawler starts with the seed URL and traverses page links at random to grow the corpus. This is justified by PageRank's model of stepping through links as a uniform probability distribution over the available links on the current page (Manning et al., 2009).

For parsing documents and queries, in the preprocessing phase, stop words are removed, all characters except alphanumeric and '-' are removed, and lowercasing is applied.

In the indexing phase, indexes are built from a search corpus using an index builder, which is trained on a training corpus. An index builder is a document vectorizer and query vectorizer, which are built with the lnc.ltc tf-idf weighting scheme. The lnc.ltc weighting scheme was found to be more effective than other variants of tf-idf from results in practice, and not convincingly theoretically justified (Buckley, 1993). Tf-idf weights terms in bag-of-words vectors with a score that takes into account how often the document includes the term and scales down the influence of terms that appear often throughout the corpus (Manning et al., 2009). The index is stored as a term-document matrix. Though inverted indices are typical efficient representations of term-to-document relationships due to sparseness, scipy implements sparse compressed matrices that offer fast computations and space effective storing. The indexer is in charge of saving index builders and indexes to files.

The query processor takes a query and a k value. It vectorizes the query and compares it to every document in the search corpus by cosine similarity, which is a length-normalized measure of the closeness in content of the bags of word (Manning et al., 2009). Documents are ranked in descending order of their similarity to the query, and the processor selects the top k documents.There is a similarity threshold of 0.02, anything below is discarded as unrelevant. 

The web application forwards the user's query and k value to the query processor, which yields the relevant documents. The application then displays them to the user. If less than k results are found, the user is notified.

## Design

![Search engine design](design.svg "Search engine design")


## Architecture

### File Structure

* Downloaded corpuses are stored in [`corpus/`](corpus) in `.jsonl` files. 
    * Each document is a JSON object with a `url` string and `text` string containing the document text.
    * Corpus names follow the structure `"corpus_prefix_name>"` + `"_items"`.
* Index builders are stored in [`index_builder/`](index_builder) in `.pkl` files.
    * Index builder names follow the structure `"<training_corpus_prefix_name>"` which matches the corpus the index builder was trained on.
* Indexes are stored in [`index/`](index) in `.pkl` files. Each is stored in a subfolder named with the `"<training_corpus_prefix_name>"` that matches the training index builder that the index was built with.
    * Index names follow the structure `"<search_corpus_prefix_name>"` which matches the corpus the index was built to search.

### Crawler

* The scrapy Spider crawler (SearchSpider) in [`crawling/crawler.py`](crawling/crawler.py) downloads web pages as JSON documents from the specified start URL using the max pages and max depth parameters.
* It uses justext to extract meaningful text from the page.
* It crawls further by following random links on the page.
* Any empty text documents or extra items are filtered out in the pipelines in [`crawling/pipelines.py`](crawling/pipelines.py).
* This crawler can be run with the specified parameters in the `scrape` function in [`crawling/scrape.py`](crawling/scrape.py), which saves the exported document items as a corpus.

### Indexer

* The functions to build and save index builders and indexes, and to load them are in [`indexer/index_utils.py`](indexer/index_utils.py) as `build_index_builder`, `build_index`, `load_index_builder`, and `load_index`.
    * Each index builder is a tuple of 2 scikit-learn TfidfVectorizers: the first for documents (lnc) and the second for queries (ltc).
    * A vectorizer stores the term vocabulary and idf values for the corpus it's trained on.
    * Each index is a term-document matrix with weighted tf-idf scores, stored as a scipy csr_matrix. This makes efficient storage and computation for sparse document vectors.

### Processor

* The query processor, in [`processor/query_processor.py`](processor/query_processor.py) has the function `get_top_k_inds_by_score`.
    * This function loads the specified training index builder and search index, and returns a ranked list of indices for the top k result documents for the given query (string) and k.
    * It applies cosine similarity between the query vector and document vectors.

### Web App

* The Flask web application in [`webapp.py`](webapp.py) has the user interface for searching.
    * Before starting up the app, the user specifies the training index builder and search corpus using each's `"<prefix_name>"`.
    * The user enters the query and k value into a `form`, which packages the query into a JSON object with a `query` string and `k_value` integer.
    * The web app validates the query/k value by assuring k is an integer above 0 and the query yields valid results (query has some text in it). It notifies the user of any errors or lack of results.
    * The web app calls the query processor with the specified training index builder and search index/corpus, and query and k value.
    * The k results are displayed to the user in order of ranked relevance.


## Operation

### Dependencies

OS used

* MacOS

Python version

* python                    3.12.2

Libraries (specifics in [requirements](requirements.txt))

* fake-useragent            1.5.1
* flask                     2.2.5
* justext                   3.0.0
* numpy                     1.26.4
* scikit-learn              1.3.0
* scrapy                    2.11.1


### Installation

Navigate to the directory containing the files in this repository.

### Executing program

Step 1:

To scrape the web to download a new corpus, specify a filename prefix for saving the corpus to a file, a seed URL/Domain, max pages, and max depth:
```
python download_corpus.py <corpus_filename_prefix> <start_url> <max_pages> <max_depth>
```
If `corpus_filename_prefix` matches an index builder that has already been built, go to step 2. 
Otherwise, skip to step 3.

Step 2:

To build an index builder trained on the corpus starting with `trained_corpus_filename_prefix` and search index of documents in the corpus starting with `search_corpus_filename_prefix`:
```
python build_index.py <trained_corpus_filename_prefix> <search_corpus_filename_prefix>
```

Step 3:

The following 2 search engine apps are available:
* `webapp.py`
* `terminal_app.py`


To run an app on a specified training corpus and search corpus, simply run:
```
python <app> <trained_corpus_filename_prefix> <search_corpus_filename_prefix>
```
This will use an index builder trained on the corpus starting with `trained_corpus_filename_prefix` for search index of documents in the corpus starting with `search_corpus_filename_prefix`.
If such an index builder/index hasn't already been built, a new one will be created.


Optional feature:

To split an existing source corpus into 2 separate corpuses, run:

```
python split_corpus.py <source_corpus_filename_prefix> <document_count1> <corpus_filename_prefix1> <document_count2> <corpus_filename_prefix2>
```
The first created corpus will have the first `document_count1` documents in the source corpus, and the second created corpus will have the following `document_count2` documents in the source corpus.

Sample first execution:

```
python download_corpus.py "whales" "https://en.wikipedia.org/wiki/Whale" 100 3
python webapp.py "whales" "whales"
```

Sample execution to rebuild index:

```
python download_corpus.py "whales" "https://en.wikipedia.org/wiki/Whale" 500 10
python build_index.py "whales" "whales"
python webapp.py "whales" "whales"
```

Sample execution to split corpus:

```
python download_corpus.py "whales" "https://en.wikipedia.org/wiki/Whale" 500 10
python split_corpus.py "whales" 400 "big-whales" 100 "small-whales"
python webapp.py "big-whales" "small-whales"
```

## Test Cases

### Framework

* PyTest (8.1.1)

### Harness

Test corpora/indexes: 

* [corpus for big whale train](corpus/big_whale_train_items.jsonl)
* [corpus for small whale test](corpus/small_whale_test_items.jsonl)
* [corpus for small test](corpus/small_test_items.jsonl)

Tests:

* [Build functionality tests](test_build.py)
* [App functionality and search functionality tests](test_output.py)

Stand-ins:
* An app created using the `create_app` function from [`webapp.py`](webapp.py)

### Coverage 

Report: [Coverage Report](https://html-preview.github.io/?url=https://github.com/marellec/SearchEngine/blob/main/coverage_re/index.html)

Build functionality:

* test that crawler downloads documents to the correct file with the correct number of documents
* test that indexer builds a valid index builder and index and saves them to the correct files
* test the index built matches the number of documents in its corpus

App functionality:

* test processing a valid query with different k values
* test processing a valid query with k that exceeds results found
* test processing a valid query that has no results
* test processing an invalid (empty) query
* test processing an invalid (negative) k
* test that when user enters a query with valid k, results page is displayed
* test that when user enters a query with invalid (negative) k, user is redirected to page to re-enter k
* test that when user enters a query with invalid (non-integer) k, user is redirected to page to re-enter k

Search functionality:

* A [training corpus](corpus/big_whale_train_items.jsonl) with 90 documents and a [test search corpus](corpus/small_whale_test_items.jsonl) with 10 documents taken from a crawl starting at the Wikipedia page for "Whale"


## Conclusion

For the test on corpuses taken from a crawl starting at the Wikipedia page for "Whale":
* Search query "people in Africa", k = 5:
    * The top 5 results contain 3 relevant documents in the search corpus: an article on [the African ethnic group Cape Coloureds](https://en.m.wikipedia.org/wiki/Cape_Coloureds), [sorghum domestication in Sudan](https://web.archive.org/web/20220520170745/https://www.journals.uchicago.edu/doi/abs/10.1086/693898?journalCode=ca), and [the Oromo people](https://en.m.wikipedia.org/wiki/Oromo_people). They appear as the first 3 results, which is promising. The first and third results are the 2 most relevant in the corpus, and the second is close, but less relevant. Of the remaining 2 results returned, the first is about an [African history project](https://en.m.wikipedia.org/wiki/General_History_of_Africa) which is close to the query, and the second is about [water scarcity](https://en.m.wikipedia.org/wiki/Water_scarcity), which completely misses the query. There is one relevant document in the corpus missing from the top 5 results about [the African island of Socotra](https://en.m.wikipedia.org/wiki/Socotra). This gives a precision of 0.6 and recall of 0.75.
* Search query "fish", k = 5:
    * Only 3 results are returned, which is promising because there is only 1 relevant document in the corpus. This document, about [a tetrapod-like fish](https://pubmed.ncbi.nlm.nih.gov/16598249/), is the first result. Of the remaining 2 results returned, the first is about [riparian zonea](https://en.m.wikipedia.org/wiki/Riparian_zone) and the second is about [the African island of Socotra](https://en.m.wikipedia.org/wiki/Socotra), which are both far from the query. This gives a precision of 0.33 and recall of 1.
* Search query "animal", k = 5:
    * Only 3 results are returned, which is again, promising, because there are only 2 relevant documents in the corpus. The most relevant document, about [a tetrapod-like fish](https://pubmed.ncbi.nlm.nih.gov/16598249/), appears as the first result, and the second most relevant, about [evolutionary relationships of two animal phyla](https://pubmed.ncbi.nlm.nih.gov/33310849/) is the second result, which makes sense. The remaining result returned is about [the African island of Socotra](https://en.m.wikipedia.org/wiki/Socotra), which is far from the query. This gives a precision of 0.66 and recall of 1.

The tests above show very high recall but low precision. This is likely because in the bag of words representation, longer documents that happen to frequently include search terms but are not primarily of that subject will have exaggerated scores. Also, longer queries match more results because more search terms means higher cosine similarity between the query and documents only containing part of the query. This can easily overinflate the number of results and increase recall at the cost of precision, as with the "people in Africa" search.

Something to be careful about with this search engine is that the crawler uses justext, which has trouble identifying titles and headers as meaningful text content. This can have an effect on scoring because titles usually have the most relevant information to the query and can repeat terms in the body text that would increase the score for a query searching for something in the title.

## Data Sources

Links

* Start url for whale test: https://en.wikipedia.org/wiki/Whale
* Start url for small test: https://en.wikipedia.org/wiki/List_of_common_misconceptions

Downloads

* [corpus for whale test](corpus/whale_test_items.jsonl) (Accessed April 22, 2024)
* [corpus for big whale train](corpus/big_whale_train_items.jsonl) (First 90 items in whale_test)
* [corpus for small whale test](corpus/small_whale_test_items.jsonl) (Last 10 items in whale_test)
* [corpus for small test](corpus/small_test_items.jsonl) (Accessed April 22, 2024)

## Resources / Attributions

* [justext](https://github.com/miso-belica/jusText)
* [StackOverflow; Author: anon01](https://stackoverflow.com/questions/68003003/python-sklearn-tfidfvectorizer-vectorize-documents-ahead-of-query-for-semantic)
* [StackOverflow; Author: matiskay](https://stackoverflow.com/questions/48042872/python-scrapy-creating-a-crawler-that-gets-a-list-of-urls-and-crawls-them)
* [StackOverflow; Author: Sunil Goyal](https://stackoverflow.com/questions/54235347/open-browser-automatically-when-python-code-is-executed)
* [README-Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)

## Bibliography (References)

* Buckley, C. (1993). The importance of proper weighting methods. *Proceedings of the Workshop on Human Language Technology  - HLT ’93.* https://doi.org/10.3115/1075671.1075753
* Manning, C. D., Raghavan, P., & Schütze, H. (2009). *An introduction to information retrieval.* Cambridge University Press. 

## Author

Marelle Leon