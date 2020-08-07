[![lifecycle](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://www.tidyverse.org/lifecycle/#experimental)
[![NSF-1928366](https://img.shields.io/badge/NSF-1928366-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1928366)

# ML Record Mining

Four-month project to create a pipeline that uses GeoDeepDive's output to find Unaquired Sites for Neotoma.  

Using NLP parsed text and a Data Science approach, identify whether a paper is suitable for Neotoma and detect features such as 'Site Name', 'Location', 'Age Span' and 'Site Descriptions'.  


## Contributors

This project is an open project, and contributions are welcome from any individual.  All contributors to this project are bound by a [code of conduct](CODE_OF_CONDUCT.md).  Please review and follow this code of conduct as part of your contribution.

  * [Simon Goring](http://www.goring.org/) [![orcid](https://img.shields.io/badge/orcid-0000--0002--2700--4605-brightgreen.svg)](https://orcid.org/0000-0002-2700-4605)
  * [Socorro Dominguez Vidana](https://sedv8808.github.io/) [![orcid](https://img.shields.io/badge/orcid-0000--0002--7926--4935-brightgreen.svg)](https://orcid.org/0000-0002-7926-4935)


### Tips for Contributing

Issues and bug reports are always welcome.  Code clean-up, and feature additions can be done either through branches.

All products of the Throughput Annotation Project are licensed under an [MIT License](LICENSE) unless otherwise noted.

## How to use this repository

Files and directory structure in the repository are as follows:
This structure might be modified as the project progresses.

```bash
throughput-ec/UnacquiredSites/
├── data
│   ├── sentences_nlp352_dummy                 # data: parsed sentences' - dummy file for reproducibility
│   ├── neotoma_dummy                          # data: paleoecology db - dummy file for reproducibility
│   └── bibjson_dummy                          # data: bibliography json dummy file for reproducibility
├── figures                                    # all docs (img/pdf)
│   ├── img
│   └── docs                       
├── database_sample.ini                        # Update with your SQL credentials
├── config_sample.py                           # Update with your computer's path
├── src    
│   ├── modules                                # all modules for the package
│   │   ├── dashboard     
│   │   │   └── record_mining_dashboard.py     # script with dashboard
│   │   ├── modelling                          # training script
│   │   │   └── model.py                       # script that creates model and predicts
│   │   └──  preprocessing                     # preprocessing of the data modules
│   │   │   ├── bibliography_loader.py         # Module to load data properly
│   │   │   ├── eda_creator.py
│   │   │   ├── neotoma_loader.py
│   │   │   ├── nlp_sentence_loader.py
│   │   │   ├── utils.py                       # Module with some utility functions
│   │   └── └── preprocess_all_data.py         # Main script for preprocessing
│   ├── output                                 # all modules for the package
│   │   ├── eda     
│   │   │   └── '*'.tsv                        # Set of 5 tsv files
│   │   ├── for_model                          
│   │   │   └── preprocessed_sentences.tsv     # File of preprocessed sentences
│   │   ├── predictions                        # training script
│   │   │   ├── comparison_file.tsv            # File with test set of sentences, their predicted label and proba
│   │   │   └── dashboard_file.tsv             # File with train set of sentences, their trained label and proba
│   │   └──  profiling                         # preprocessing of the data modules
│   │   │   ├── profiling_model.txt            # File with detailed profile of model script
│   │   │   └── profiling_preprocess_data.tsv  # File with detailed profile of preprocess_data script
│   └── tests                                  # all tests for the modules
│   │   ├── test_data                                       
│   │   ├── test_bibliography_loader.py                      
│   │   ├── test_eda_creator.py
│   │   ├── test_neotoma_loader.py
│   │   ├── test_nlp_sentence_loader.py
│   │   ├── test_utils.py                                   
│   │   └── test_preprocess_all_data.py  
├── .gitignore
├── CODE_OF_CONDUCT.md
├── Dockerfile
├── LICENSE
├── makefile
└── README.md
```

### Workflow Overview

This project uses the GeoDeepDive output files:
* `sentences_nlp352:` sentences file that contains NLP parsed sentences.
* `bibjson:` JSON file that contains bibliographic information.
* `neotoma:` tsv file that contains Netoma paleoecology database information.

These files are used as input in a ML model that, once trained, should:
* Predict whether a sentence has coordinates or not in it.

TODO
* Pull appropriately the coordinates.
* Improve the Site Name, Location, Age Span and Site Descriptions.

### System Requirements

This project is developed using Python.  
It runs on a MacOS system.
Continuous integration uses TravisCI.

### Data Requirements

The project pulls data from GeoDeepDive output files.
For the sake of reproducibility, three dummy data files have been included.

### Key Outputs

This project will generate a dataset that provides the following information:
* Whether the paper is useful for Neotoma.
* Site Name, Location, Age Span and Site Descriptions from paper.

### Instructions
##### Docker

To run this analysis using Docker:

1. Clone/download this repository
2. Use the command line on your computer to get the [unacquiredsites](https://hub.docker.com/r/sedv8808/unacquiredsites) image from [DockerHub](https://hub.docker.com/):
```
docker pull sedv8808/unacquiredsites
```
3. Use the command line to navigate to the root of this project on your computer, and then type the following (filling in *\<Path_on_your_computer\>* with the absolute path to the root of this project on your computer).
```
docker run --rm -v <Path_on_your_computer>:/UnacquiredSites  sedv8808/unacquiredsites make -C '/UnacquiredSites' all
```

4. To clean up the analysis type:
```
docker run --rm -v <Path_on_your_computer>:/UnacquiredSites  sedv8808/unacquiredsites make -C '/UnacqiredSites' clean
```

##### Without Docker

This repository consists of 3 Python scripts.
<br>
Use this `Makefile` to generate a model that will help identify if a Sentence has 'coordinates' in it or not.
<br>

In order to run this project, you need to:
1. Clone or download this repository.

2. Run the following code in the terminal at the project's root repository.
To run the scripts:

```
# From the command line.

# To run all the Python scripts from beginning to the end. Delivers a final report.
make all

#	Deletes all unnecessary files in case you need to run the project from scratch.
make clean

```
The makefile is the short way of running all Python scripts in the following order :

```
# Load data and Exploratory Data Analysis
python3 src/modules/preprocessing/preprocess_all_data.py

# Train model or use trained model for inference
python3 src/modules/modelling/model.py --trained_model='yes'

# Summarize and visualize data
python3 src/modules/dashboard/record_mining_dashboard.py

# To visualize in your browser, enter the following http address.
http://127.0.0.1:8050/


# TODO
Write reports
```

##  Profiling
Detailed profiling logs can be found on:
```
src/output/profiling
```

If you want to repeat a detailed profiling for each script, open `preprocess_all_data.py` and `model.py`.
Both scripts, at the bottom, have a commented chunk of code titled `Profiling`.
This profiling is recommended to only be run once. Once you finished this, comment the chunk again.
** TODO: Add args function in scripts to decide whether or not to do the profiling.

#### preprocess_all_data.py



## Instructions
Review src README file to run the python package for inference.
