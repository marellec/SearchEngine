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

To scrape the web to download a new corpus and build a corresponding index, specify
seed URL/Domain, max pages, and max depth:
```
python build.py <start_url> <max_pages> <max_depth>
```

Optionally, specify a save filename prefix for saving the corpus and index to files:
```
python build.py <start_url> <max_pages> <max_depth> <save_filename_prefix>
```

The following 2 search engine apps are available:
* webapp.py
* terminal_app.py

After downloading the corpus and building the index, to run an app, run:
```
python <app>
```

To run an app on a specified downloaded corpus and built index, simply run:
```
python <app> <save_filename_prefix>
```
This will use the corpus and corresponding index starting with the given prefix.


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

Pages are open source.

[Start_url_for_default_build]()
[Start_url_for_one_test]()
[Start_url_for_small_test]()

[data_for_default_build]()
[data_for_one_test]()
[data_for_small_test](corpus/small_test_items.json)

## Resources

* [justext](https://github.com/miso-belica/jusText)
* [README-Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)



## Bibliography (References)



## Authors

Marelle Leon