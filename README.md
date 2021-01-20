[![lifecycle](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://www.tidyverse.org/lifecycle/#experimental)
[![NSF-1928366](https://img.shields.io/badge/NSF-1928366-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1928366)

# ML Record Mining

Project that creates a pipeline that uses GeoDeepDive's output to find Unaquired Sites for Neotoma.  

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
├── img                                        # all images used in README or reports      
├── output                                 # all modules for the package
│   ├── eda     
│   │   └── '*'.tsv                        # Set of 5 tsv files
│   ├── preprocessed_data                  
│   │   └── preprocessed_sentences.tsv     # File of preprocessed sentences
│   ├── predictions                        # Predictions from trained model (train/new data sets)
│   └──  profiling                         # preprocessing of the data modules
│   │   ├── profiling_model.txt            # File with detailed profile of model script
│   └── └── profiling_preprocess_data.tsv  # File with detailed profile of preprocess_data script   
│   ├── count_vec_model.sav                # CountVectorizer saved model
│   ├── NB_model.sav                       # NaiveBayes saved model
├── reports                                # Milestone results/ Method descriptions
├── src  
│   ├── modules                            # all modules for the package
│   │   ├── modelling                      # training script
│   │   │   └──  model.py                  # script that creates model and predicts
│   │   ├── predicting                     # script to do predictions on new data
│   │   │   └──  utils.py                  # auxiliary functions
│   │   │   └──  predict.py                # prediction script for new data
│   │   ├── preprocessing                  # directory for preprocessing data
│   │   │   ├── bibliography_loader.py     # Module to load data properly
│   │   │   ├── eda_creator.py             # Preliminary EDA creator
│   │   │   ├── neotoma_loader.py
│   │   │   ├── nlp_sentence_loader.py
│   │   │   ├── utils.py                   # Module with some utility functions
│   │   └── └── preprocess_all_data.py     # Main script for preprocessing
│   ├── tests                              # all tests for the modules
│   │   ├── test_data                                       
│   │   ├── test_bibliography_loader.py                      
│   │   ├── test_eda_creator.py
│   │   ├── test_neotoma_loader.py
│   │   ├── test_nlp_sentence_loader.py
│   │   ├── test_utils.py                                   
│   └── └── test_preprocess_all_data.py  
│   ├── config_sample.py                   # config to load to SQL
│   ├── database_sample.ini                # config to load to SQL
├── CODE_OF_CONDUCT.md
├── ml.Dockerfile
├── LICENSE
└── README.md
```

### Workflow Overview

This project uses the GeoDeepDive output files:
* `sentences_nlp352:` sentences file that contains NLP parsed sentences.
* `bibjson:` JSON file that contains bibliographic information.
* `neotoma:` tsv file that contains Netoma paleoecology database information.

These files are used as input in a ML model that, once trained, should:
* Predict whether a sentence has coordinates or not in it.

Next steps include:
* Build a model that extracts the coordinates.
* Improves the Site Name, Location, Age Span and Site Descriptions.

### System Requirements
This project is developed using Python.  
It runs on a MacOS system.
Continuous integration uses TravisCI.

### Data Requirements
The project pulls data from GeoDeepDive output files.
For the sake of reproducibility, three dummy data files have been included.

### Key Outputs
This project will generate a dataset that provides the following information:
* Whether the paper has or not coordinates.
* A file that will be used in the Dashboard repository to correct and handlabel missing data.

## Pipeline
The current pipeline that is followed is:
\n
\n

![img](img/RMFlow.jpg)


### Instructions
##### Docker ML Predict

If you are trying to get new predictions on never seen corpus, then follow these instructions:

1. Clone/download this repository.
2. Put your input data in the data file. The dummy files have been included.
3. Using the command line, go to the root directory of this repository.
4. Get the [unacquired_sites_ml_app](https://hub.docker.com/r/sedv8808/unacquired_sites_ml_app) image from [DockerHub](https://hub.docker.com/) from the command line:
```
docker pull sedv8808/unacquired_sites_ml_app:latest
```
4. Verify you are in the root directory of this project. Type the following (filling in *\<Path_on_your_computer\>* with the absolute path to the root of this project on your computer).

```
docker run -v <User's Path>/sentences_nlp352:/app/input/sentences -v <User's Path>/bibjson:/app/input/biblio -v <User's Path>/predictions/:/app/output/predictions/ sedv8808/unacquired_sites_ml_app:latest
```
5. You will get an output file with a timestamp. That file are your predictions. You can load that file into the dashboard to verify if the sentences that seem to have coordinates make sense.

You can find the Dashboard repository [here](https://github.com/throughput-ec/UnacquiredSitesDashboard)

**IMPORTANT:** In order to run this docker file, you need to load in the `data` directory a `bibjson` file and a `sentences_nlp3522` that respect the same format as the dummy files.

##### Without Docker and to view/modify other scripts.

This repository consists of 3 main modules: Preprocessing, Modelling, Predicting.

In order to run this project, you need to:
1. Clone or download this repository.

2. Run the following code in the terminal at the project's root repository.
To run the scripts:

```
# From the command line.

# Load data and Exploratory Data Analysis
python3 src/modules/preprocessing/preprocess_all_data.py

# Train model and export Training Metrics
python3 src/modules/modelling/model.py --eda_file='yes'

# Predict on new data
python3 src/modules/predicting/predict.py
```

##  Profiling
Detailed profiling logs can be found on:
```
output/profiling
```

If you want to repeat a detailed profiling for each script, open `preprocess_all_data.py` and `model.py`.
Both scripts, at the bottom, have a commented chunk of code titled `Profiling`.
This profiling is recommended to only be run once. Once you finished this, comment the chunk again.


#### preprocess_all_data.py
Used timeit function with Python.
I took random samples of 1000, 10000 to see speed.
To increase data, I appended the same NLPSentence file 3 times. Ideally, would want to try with other data.
Bibjson and Neotoma databases where used complete as those bases cannot be trimmed (Risk of missing joins)
| n_sentences |  tot_time  |  
| ----------- | ---------- |  
|     1000    |    0.000   |
|    10000    |    0.001   |
|   112720    |    4.578   |
|   338160    |   12.732   |


#### model.py
Used timeit function with Python.
I took random samples of 1000, 10000 and total number of sentences to train dataset.
Always choose to train the model from scratch. Did not do profiling if a pretrained model was chosen.
Did not increase data.
| n_sentences |  tot_time  |  
| ----------- | ---------- |  
|     1000    |    0.000   |
|    10000    |    1.001   |
|   106640    |   12.732   |
