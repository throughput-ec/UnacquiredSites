import argparse
import os
import cProfile
import pstats
import io
import pandas as pd
import json
#import utils as ard
#import bibliography_loader as bl

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import time
import pickle

import argparse
import sys
import os

import cProfile, pstats, io

## USAGE
## python3 src/modules/modelling/predict.py \
## --input_name = 'data/sentences_nlp3522' \
## --bib_file = 'data/bibjson2' \
## --output_file='src/output/predictions/predicted_labels_new_data.tsv'

file = r'data/sentences_nlp3522'
bib_file = r'data/bibjson2'
out_file_name = r'src/output/predictions/predicted_labels_new_data.tsv'

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_name', type=str, default=file,
                        help='Path + Name of the file as tsv.')
    parser.add_argument('--bib_file', type=str, default=bib_file,
                        help='Directory where bibliography json file is.')
    parser.add_argument('--output_file', type=str, default=out_file_name,
                        help='Directory where your output data is.')

    args = parser.parse_args()

    nlp_sentences = preprocessed_sentences_csv(args.input_name)
    bibliography = bibliography_loader(args.bib_file)
    nlp_bib = nlp_sentences.merge(bibliography, on='_gddid')
    original_sentences = nlp_bib[['_gddid', 'title', 'sentid','words_as_string', 'link_url']]

    y_pred, y_proba = predict(data_test = nlp_bib)

    guessed_label = pd.DataFrame(y_pred)

    predicted_proba = pd.DataFrame(y_proba)

    original_sentences = original_sentences.reset_index()

    test_pred_comp = pd.merge(guessed_label, predicted_proba, left_index=True, right_index=True)

    test_pred_comp = pd.merge(original_sentences, test_pred_comp, left_index=True, right_index=True)
    test_pred_comp = test_pred_comp.reset_index(drop=True)
    test_pred_comp = test_pred_comp.rename(columns={'0_x':'guessed_label', '0_y':'predicted_proba'})

    test_pred_comp = test_pred_comp[['sentid','words_as_string', 'link_url', 'guessed_label', 'predicted_proba', '_gddid', 'title']]

    output_file = os.path.join(args.output_file)
    test_pred_comp.to_csv(output_file, sep='\t', index = False)
    print(f"Saving predictions: {output_file}")

def convert_words_to_string(df,
                            col_to_convert='col',
                            new_col_name='words_as_string'):
    """
    Converts list of strings into a single string

    Parameters
    ----------
    df : pd.DataFrame
        Input data frame
    col_to_convert : df column
        Column that contains list of strings
    new_col_name : df column
        Name of the new column

    Returns
    -------
    pd.DataFrame with new column
    This new column contains the list of strings converted to just one string.
    """

    df[new_col_name] = df[col_to_convert]\
        .apply(lambda x: ','.join(map(str, x)))

    return df

def bibliography_loader(path):
    """
    Loads and formats bibliography json file and converts to a dataframe

    Parameters
    ----------
    path : string
        Path where the bibliography database is stored.

    Returns
    -------
    bibliography: pd.DataFrame
        pd.DataFrame with all bibliography information
    """
    with open(path, 'r') as f:
        bib_dict = json.load(f)
    # Normalizing data so that we have access to the 'identifier'
    [elem.update({'identifier':[{'_type':None,'_id':None}]}) for elem in bib_dict if 'identifier' not in elem.keys()]

    # TODO Load into SQL server and connect through SQL
    bibliography = pd.io.json.json_normalize(bib_dict,
                                             'identifier',
                                             ['publisher', 'title',
                                              ['journal', 'name', 'name'],
                                              ['author'],
                                              'year', 'number', 'volume',
                                              ['link'],
                                              '_gddid', 'type', 'pages'],
                                             record_prefix='_',
                                             errors='ignore')

    bibliography['link'] = bibliography['link'].astype(str)

    url = bibliography['link'].str.split(", ", expand=True)

    bibliography['link_url'] = url[0]
    bibliography['link_type'] = url[1]

    bibliography['link_url'] = bibliography['link_url']\
        .replace(r"\[{'url': '", "", regex=True)\
        .replace("'", "", regex=True)

    bibliography['link_type'] = bibliography['link_type']\
        .replace("'type': '", "", regex=True)\
        .replace("'}]", "", regex=True)

    bibliography['author'] = bibliography['author'].astype(str)
    bibliography['author'] = bibliography['author']\
        .replace(r"\[{'name': '", "", regex=True)\
        .replace("{'name': '", "", regex=True)\
        .replace("'},", ";", regex=True)\
        .replace("'}]", "", regex=True)

    bibliography = bibliography[['_id', 'publisher', 'title',
                                 'author', 'year', 'number',
                                 'volume', '_gddid', 'type',
                                 'pages', 'link_url']]

    bibliography = bibliography.rename(columns={'_id': 'doi'})

    return bibliography

def preprocessed_sentences_csv(path = file):
    header_list = ["_gddid", "sentid", "wordidx", "words", "part_of_speech", "special_class",
               "lemmas", "word_type", "word_modified"]
    nlp_sentences = pd.read_csv(path, sep='\t', names = header_list)
    nlp_sentences = nlp_sentences[['_gddid', 'sentid', 'words']]
    nlp_sentences = nlp_sentences.replace('"', '', regex = True)\
                                 .replace('\{', '', regex = True)\
                                 .replace('}', '', regex = True)\
                                 .replace(',', ',', regex = True)\
                                 .replace(r'\W{4,}', '', regex=True)\
                                 .replace(',,,', 'comma_sym', regex=True)\
                                 .replace(',', ' ', regex=True)\
                                 .replace('comma_sym', ', ', regex=True)\
                                 .replace('-LRB- ', '(', regex=True)\
                                 .replace('LRB', '(', regex=True)\
                                 .replace(' -RRB-', r')', regex=True)\
                                 .replace('RRB', r')', regex=True)\
                                 .replace('-RRB', r')', regex=True)
    nlp_sentences['words']= nlp_sentences['words'].str.split(",")
    # Sentences - not words.
    nlp_sentences = convert_words_to_string(nlp_sentences, col_to_convert = 'words', new_col_name = 'words_as_string')
    return nlp_sentences


def predict(data_test):
    vec = pickle.load(open('src/output/count_vec_model.sav', 'rb'))
    X_test = vec.transform(data_test['words_as_string'].fillna(' '))
    loaded_model = pickle.load(open('src/output/finalized_model.sav', 'rb'))
    y_pred = loaded_model.predict(X_test)
    y_proba = loaded_model.predict_proba(X_test)[:,1]
    return y_pred, y_proba

if __name__ == '__main__':
    main()
