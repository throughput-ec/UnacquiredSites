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
│   ├── sentences_nlp352                                    # data: parsed sentences' dummy file for reproducibility
│   └── bibjson                                             # data: bibliography json dummy file for reproducibility
├── figures                                                 # all docs (md/pdf)
│   ├── charts
│   └── docs                       
├── src    
│   ├── README.md     
│   ├── database_sample.ini                                 # dummy file to show the format for your ini file
│   ├── config_sample.py                                    # dummy file to show the format for your config file
│   ├── modules                                             # all modules for the package
│   │   ├── dashboard                                       # module for dashboard
│   │   ├── eda_creator                                     # eda_creator for Jupyter Notebook files
│   │   ├── modelling                                       # training script
│   │   │   └── stat_test_result
│   │   └──  preprocessing                                  # preprocessing of the data modules
│   └── tests                                               # all tests for the modules
│       └── test_data
└── README.md
```

### Workflow Overview

This project uses the GeoDeepDive output files:
* `sentences_nlp352:` sentences file that contains NLP parsed sentences.
* `bibjson:` JSON file that contains bibliographic information.

These files are used as input in a ML model that, once trained, should:
* Predict whether the paper is suitable for Neotoma.
* Improve the Site Name, Location, Age Span and Site Descriptions.


### System Requirements

This project is developed using Python.  
It runs on a MacOS system.
Continuous integration uses TravisCI.

### Data Requirements

The project pulls data from GeoDeepDive output files.
For the sake of reproducibility, two dummy data files have been included.


### Key Outputs

This project will generate a dataset that provides the following information:
* Whether the paper is useful for Neotoma.
* Site Name, Location, Age Span and Site Descriptions from paper.


## Instructions
Review src README file to run the python package for inference.
