# README

## Input Data

The input data can be done either by a text file or by connecting a Postgresql server.

If the latter is used, the data will be loaded using the `config` and `database.ini` as initialization files.

`database.ini` holds all the credentials to log in to the postgresql server and should be included in the `.gitignore` file.  `database.ini` is located in the src directory.

To do your own `database.ini` file, just copy and paste the text bellow and change the credentials accordingly.

[postgresql]  
user = user  
password = pwd  
host = localhost  
port = 5432  
database = database


On the config.py file, you should also edit the route you are loading `database.ini` from.

You can use the sample files attached in this repository.


## Preprocessing the Data Instructions

```
python3 /Users/user/path/where/script/is/UnacquiredSites/src/modules/preprocessing/preprocess_all_data.py \
## --output_path='/Users/user/desired/path/for/output' --output_name='sample_name.tsv'
## --bib_file='/Users/user/path/where/file/is/bibjson' --neotoma_file='/Users/user/path/where/file/is/data-1590729612420.csv'
```

## Training the Model Instructions

You can load a trained model or retrain the model. For this, change the argsparse option --trained_model to yes or no.
```
python3 Users/user/path/where/script/is/UnacquiredSites/src/modules/modelling/model.py \
## --input_path = '/Users/user/output/path/UnacquiredSites/src/output/for_model' \
## --input_file = 'preprocessed_sentences.tsv' \
## --trained_model='yes'
```
A file with prediction will be saved in the same path. This way, the final results can be compared easier.
This file also feeds the Dashboard.
