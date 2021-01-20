import argparse
import os
import cProfile
import pstats
import io
import pandas as pd
import json
import utils as utils


from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

import time
import pickle

import argparse
import sys
import os

import cProfile, pstats, io

import warnings
warnings.filterwarnings("ignore")

## USAGE
## python3 src/modules/modelling/predict.py \
## --input_name = 'data/sentences_nlp3522' \
## --bib_file = 'data/bibjson2' \
## --output_file='output/predictions/predicted_labels_new_data.tsv'

file = r'data/sentences_nlp3522'
bib_file = r'data/bibjson2'
out_file = r'output/predictions/'
t = time.localtime()
timestamp = time.strftime('%b_%d_%Y_%H%M%S', t)
out_file_name = r'predictions_new_data_'+timestamp+'.tsv'

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_name', type=str, default=file,
                        help='Path + Name of the file as tsv.')
    parser.add_argument('--bib_file', type=str, default=bib_file,
                        help='Directory where bibliography json file is.')
    parser.add_argument('--output_file', type=str, default=out_file,
                        help='Directory where your output data is.')

    args = parser.parse_args()

    nlp_sentences = preprocessed_sentences_tsv(args.input_name)
    bibliography = preprocessed_bibliography(args.bib_file)
    nlp_bib = nlp_sentences.merge(bibliography, on='gddid')
    original_sentences = nlp_bib[['gddid', 'title', 'sentid','sentence']]
    y_pred, y_proba = predict(data_test = nlp_bib)

    predicted_label = pd.DataFrame(y_pred)
    prediction_proba = pd.DataFrame(y_proba)
    original_sentences = original_sentences.reset_index()

    prediction_comp = pd.merge(predicted_label, prediction_proba, left_index=True, right_index=True)
    prediction_comp = pd.merge(original_sentences, prediction_comp, left_index=True, right_index=True)
    prediction_comp = prediction_comp.reset_index(drop=True)
    prediction_comp = prediction_comp.rename(columns={'0_x':'predicted_label', '0_y':'prediction_proba'})
    prediction_comp = prediction_comp[['sentid','sentence', 'predicted_label', 'prediction_proba', 'gddid', 'title']]

    selection1 = prediction_comp[(prediction_comp['prediction_proba'] > 0.000) & (prediction_comp['prediction_proba'] < 0.1)]
    selection1 = selection1.sample(frac = 0.15)
    selection2 = prediction_comp[prediction_comp['prediction_proba'] >= 0.1]
    prediction_comp = pd.concat([selection1, selection2])
    prediction_comp['true_label']='unknown'
    prediction_comp['found_lat']='unknown'
    prediction_comp['latnorth']='unknown'
    prediction_comp['found_long']='unknown'
    prediction_comp['longeast'] = 'unknown'
    prediction_comp['Train/Pred']='Pred'

    prediction_comp = prediction_comp[['gddid', 'title', 'sentid', 'sentence', 'predicted_label', 'prediction_proba', 'true_label', 'found_lat', 'latnorth', 'found_long', 'longeast', 'Train/Pred']]
    prediction_comp.sort_values(by=['gddid', 'sentid'], inplace = True)

    output_file = os.path.join(args.output_file, out_file_name)
    prediction_comp.to_csv(output_file, sep='\t', index = False)

    print(f"Saving predictions: {output_file}")

def preprocessed_bibliography(path):
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

    bibliography = pd.json_normalize(bib_dict,
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

    bibliography = bibliography[['_type', '_id', 'publisher', 'title',
                                 'journal.name.name',
                                 'author',
                                 'year', 'number', 'volume',
                                 '_gddid', 'type', 'pages',
                                 'link_url', 'link_type']]

    bibliography = bibliography.rename(columns={'_id': 'doi', '_gddid':'gddid'})

    return bibliography

def preprocessed_sentences_tsv(path = file):
    nlp_sentences = pd.read_csv(path, sep='\t', names = ['gddid', 'sentid', 'wordidx', 'words', 'part_of_speech', 'special_class',
               'lemmas', 'word_type', 'word_modified'], usecols = ['gddid', 'sentid', 'words'])
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
    nlp_sentences['sentence'] = nlp_sentences['words'].apply(lambda x: ','.join(map(str, x)))

    # REGEX Values
    nlp_sentences = utils.find_regex(nlp_sentences, find_val = 'dms_regex',\
                                search_col = 'sentence', new_col_name = 'dms_re')
    nlp_sentences = utils.find_regex(nlp_sentences, find_val = 'dd_regex',\
                                search_col = 'sentence', new_col_name = 'dd_re')
    nlp_sentences = utils.find_regex(nlp_sentences, find_val = 'digits_regex',\
                                search_col = 'sentence', new_col_name = 'digits_re')

    # NLP Taks
    stop = stopwords.words('english')
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    stemmer = SnowballStemmer("english")

    nlp_sentences['nltk'] = nlp_sentences.apply(lambda row: tokenizer.tokenize(row['sentence']), axis=1)
    nlp_sentences['nltk']=nlp_sentences['nltk'].apply(lambda x: [item for item in x if item not in stop])
    nlp_sentences['nltk']=nlp_sentences['nltk'].apply(lambda x: [stemmer.stem(y) for y in x])
    nlp_sentences = nlp_sentences[['gddid', 'sentid', 'sentence', 'nltk', 'dms_re', 'dd_re', 'digits_re']]

    return nlp_sentences


def predict(data_test):
    vec = pickle.load(open('output/count_vec_model.sav', 'rb'))
    X_test = vec.transform(data_test['sentence'].fillna(' '))

    loaded_model = pickle.load(open('output/NB_model.sav', 'rb'))
    y_pred = loaded_model.predict(X_test)
    y_proba = loaded_model.predict_proba(X_test)[:,1]
    return y_pred, y_proba

if __name__ == '__main__':
    main()
