# Project Title

Abstract - Development summary, objectives, and next steps.

## Description

Overview - Solution outline, relevant literature, proposed system.

## Design

Design - System capabilities, interactions, integration.



## Architecture
 
Architecture - Software components, interfaces, implementation.



## Getting Started

### Dependencies

OS used

* MacOS

Python version

* python                    3.12.2

Libraries (specifics in requirements.txt)

* fake-useragent            1.5.1
* flask                     2.2.5
* justext                   3.0.0
* numpy                     1.26.4
* scikit-learn              1.3.0
* scrapy                    2.11.1

### Installing

inputs, installation

* How/where to download your program
* Any modifications needed to be made to files/folders




### Executing program

The following 2 search engine apps are available:
* webapp.py
* terminal_app.py

To scrape the web to download a new corpus, specify
seed URL/Domain, max pages, and max depth:
```
python <app> <start_url> <max_pages> <max_depth>
```

Optionally, specify a save filename prefix for saving the corpus and index to files:
```
python <app> <start_url> <max_pages> <max_depth> -n <save_filename_prefix>
```

To run the app without downloading a new corpus (and building a new index), simply run:
```
python <app> -n <save_filename_prefix>
```
This will use the index corresponding to the corpus starting with the given prefix.


## Conclusion

Conclusion - Success/Failure results, outputs, caveats/cautions.


### Test Cases

Test Cases - Framework, harness, coverage.

Framework

* PyTest (8.1.1)

Harness



(+ test files and stuff)


Coverage 




## Data Sources

Data Sources - Links, downloads, access information.


## Resources

* [README-Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)



## Bibliography (References)



## Authors

Marelle Leon