[![lifecycle](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://www.tidyverse.org/lifecycle/#experimental)
[![NSF-1928366](https://img.shields.io/badge/NSF-1928366-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1928366)

# Unacquired Sites

Four-month project to create a pipeline that allows to detect Site Name, Location, Age Span and Site Descriptions from papers in the Neotoma Data Base.
Use NLP processed text and a Data Science approach and detect whether the paper is suitable for Neotoma Data Base.

  * Please define which data products

## Contributors

This project is an open project, and contributions are welcome from any individual.  All contributors to this project are bound by a [code of conduct](CODE_OF_CONDUCT.md).  Please review and follow this code of conduct as part of your contribution.

  * [Simon Goring](http://www.goring.org/) [![orcid](https://img.shields.io/badge/orcid-0000--0002--2700--4605-brightgreen.svg)](https://orcid.org/0000-0002-2700-4605)
  * [Socorro Dominguez Vidana](https://sedv8808.github.io/) [![orcid](https://img.shields.io/badge/orcid-0000--0002--7926--4935-brightgreen.svg)](https://orcid.org/0000-0002-7926-4935)


### Tips for Contributing

Issues and bug reports are always welcome.  Code clean-up, and feature additions can be done either through pull requests to [project forks]() or branches.

All products of the Throughput Annotation Project are licensed under an [MIT License](LICENSE) unless otherwise noted.

## How to use this repository

Files and directory structure in the repository are as follows:
This structure might be modified as the project progresses.

```bash
throughput-ec/UnacquiredSites/
├── data
│   ├── sentences_nlp352                                    # data: parsed sentences' dummy file for reproducibility
│   └── bibjson                                             # data: bibliography json dummy file for reproducibility
├── docs                                                    # all docs (md/pdf)
│   ├── 200615_monthly_report
│   ├── 200715_monthly_report
│   ├── 200815_monthly_report
│   ├── 200915_monthly_report
│   └── 00_user_manual                       
└── model_that_locates_sites/location/etc                                    
    ├── modules                                          # all modules for the package
    │   ├── arch                                             # model architectures used
    │   ├── dataloader                                       # dataloader + related files
    │   ├── output                                           # preprocessing output
    │   │   └── stat_test_result
    │   └──  preprocessing                                   # preprocessing modules
    └── tests                                                # all tests for the modules
        └── test_data
```

### Workflow Overview

This project uses the Neotoma GeoDeepDive output files; the sentences_nlp352 (sentences file that contains NLP parsed sentences) and the bibjson (JSON file that contains bibliographic information) as input.

This files should then train a model that will then
- Using additional features, improve the Site Name, Location, Age Span and Site Descriptions.
- Predict whether the paper is suitable for the Neotoma Data Base.


### System Requirements

This project is developed using Python.  
It runs on a MacOS system.
Continuous integration uses TravisCI.

### Data Requirements

The project pulls data from GDD output files.

### Key Outputs

This project will generate a dataset that provides Site Name, Location, Age Span and Site Descriptions from papers in the Neotoma Data Base.

## Metrics

This project is to be evaluated using the following metrics:
