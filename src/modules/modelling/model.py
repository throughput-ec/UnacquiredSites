import pandas as pd
import numpy as np
import random

# Loading libraries for modeling
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
## python3 src/modules/modelling/model.py \
## --input_file = 'src/output/for_model/preprocessed_sentences.tsv' \
## --trained_model='yes'

in_file_name = r'src/output/for_model/preprocessed_sentences.tsv'

out_file_name = r'src/output/predictions/comparison_file.tsv'


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_file', type=str, default=in_file_name,
                        help='Directory where your input data is.')

    parser.add_argument('--output_file', type=str, default=out_file_name,
                        help='Directory where your input data is.')

    parser.add_argument('--trained_model', type=str, default='yes',
                        help='Use train model or no. Options: yes/no')

    args = parser.parse_args()


    X_train, y_train, X_test, y_test, data_test = prepare_data(file = args.input_file)
    print("Using CountVectorizer to normalize data...")

    # Start predictions
    print("Getting ready for predictions...")

    if args.trained_model == 'yes':
        print("Loading previous model")

        y_pred, y_proba = predict(X_test, y_test, X_train, y_train, trained_model = 'yes')
        print("Completed predictions")

    if args.trained_model == 'no':
        print("Training again...")
        y_pred, y_proba = predict(X_test, y_test, X_train, y_train, trained_model = 'no')
        print("Getting predictions...")
        print("Completed predictions!")

    guessed_label = pd.DataFrame(y_pred)
    actual_label = pd.DataFrame(y_test)
    predicted_proba = pd.DataFrame(y_proba)
    actual_label = actual_label.reset_index()

    original_sentence = pd.DataFrame(data_test[['_gddid','sentid','words_as_string', 'found_lat', 'latnorth', 'found_long', 'longeast', 'found_sites']])
    original_sentence = original_sentence.reset_index()

    test_pred_comp = guessed_label.join(actual_label)
    test_pred_comp = test_pred_comp.drop(columns=['index'])
    test_pred_comp.columns = ['predicted_label'] + test_pred_comp.columns.tolist()[1:]

    test_pred_comp = predicted_proba.join(test_pred_comp)
    test_pred_comp.columns = ['prediction_proba'] + test_pred_comp.columns.tolist()[1:]
    #test_pred_comp = test_pred_comp.drop(columns=['index'])

    test_pred_comp = test_pred_comp.join(original_sentence)
    test_pred_comp = test_pred_comp.drop(columns=['index'])
    test_pred_comp = test_pred_comp.rename(columns={'0':'predicted_proba', 'has_both_lat_long_int':'original_label', 'words_as_string':'sentence'})
    #test_pred_comp.columns = ['predicted_proba'] + test_pred_comp.columns.tolist()[1:]

    output_file = os.path.join(args.output_file)
    test_pred_comp.to_csv(output_file, sep='\t', index = False)
    print(f"Saving validation - prediction comparison dataframe in: {output_file}")

    #print(test_pred_comp['predicted_proba'])

def prepare_data(file = in_file_name):
    input_file = file
    df = pd.read_csv(input_file, sep='\t')

    df['has_both_lat_long_int'] = ((df['found_lat'].apply(len) > 2) & (df['found_long'].apply(len) > 2 ))

    # Map True to One and False to Zero
    df['has_both_lat_long_int'] = df['has_both_lat_long_int'].astype(int)

    # Balancing data
    random.seed(30)
    df0 = df[df['has_both_lat_long_int'] == 0]
    df0 = df0.sample(n = 600, random_state=1)
    df1 = df[df['has_both_lat_long_int'] == 1]
    df = pd.concat([df0, df1])


    # Reduce data to columns of interest for this task.
    # df = df[['words_as_string', 'has_both_lat_long_int']]

    # Define corpus for CountVectorizer
    #corpus = df['words_as_string'].tolist()

    # Split data into training and testing sets
    data_train, data_test = train_test_split(df, test_size = 0.20, random_state = 12)

    # Translate words to vectors
    # NLP model
    vec = CountVectorizer(min_df=2,
                          tokenizer=nltk.word_tokenize)

    # Fit and transform training
    X_train = vec.fit_transform(data_train['words_as_string'].fillna(' '))
    y_train = data_train['has_both_lat_long_int']

    # Transform test data without fitting
    X_test = vec.transform(data_test['words_as_string'].fillna(' '))
    y_test = data_test['has_both_lat_long_int']

    return X_train, y_train, X_test, y_test, data_test

#X_train, y_train, X_test, y_test, data = prepare_data(path = path, data_file = data_file)


def train(X_train, y_train):
    clf = DecisionTreeClassifier(min_samples_split = 40, max_depth = 12)
    clf.fit(X_train, y_train)
    filename = 'src/output/finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    return clf


def predict(X_test, y_test, X_train, y_train, trained_model = 'yes'):
    if trained_model == 'yes':
        loaded_model = pickle.load(open('src/output/finalized_model.sav', 'rb'))
        training_acc = loaded_model.score(X_train, y_train)
        print(f"This model's training accuracy was of: {training_acc:.5f}")
        result = loaded_model.score(X_test, y_test)
        print(f"Model's validation accuracy: {result:.5f}")
        y_pred = loaded_model.predict(X_test)
        y_proba = loaded_model.predict_proba(X_test)[:,1]
        return y_pred, y_proba

    if trained_model == 'no':
        print("Retraining the model")
        model = train(X_train, y_train)
        print("Updated final model.")
        training_acc = model.score(X_train, y_train)
        print(f"Model's training accuracy: {training_acc:.5f}")
        result = model.score(X_test, y_test)
        print(f"Model's validation accuracy: {result:.5f}")
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:,1]
        return y_pred, y_proba

# Uncomment for profiling
#pr = cProfile.Profile()
#pr.enable()

#my_result = main()

#pr.disable()
#s = io.StringIO()
#ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
#ps.print_stats()

#with open('src/output/profiling/profiling_model.txt', 'w+') as f:
#    f.write(s.getvalue())

if __name__ == '__main__':
    main()
