import pandas as pd
import numpy as np

# Loading libraries for modeling
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import time
import pickle

import os
path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output'
data_file = r'completed_preprocessing.tsv'
file = path + '/' + data_file


def prepare_data(file = file):
    df = pd.read_csv(file, sep='\t')

    df['has_both_lat_long_int'] = ((df['intersection_words_lat'].apply(len) > 2) & (df['intersection_words_long'].apply(len) > 2 ))

    # Map True to One and False to Zero
    df['has_both_lat_long_int'] = df['has_both_lat_long_int'].astype(int)

    # Reduce data to columns of interest for this task.
    df = df[['words_as_string', 'has_both_lat_long_int']]

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

    return X_train, y_train, X_test, y_test, df

#X_train, y_train, X_test, y_test, data = prepare_data(path = path, data_file = data_file)


def train(X_train, y_train):
    clf = DecisionTreeClassifier(min_samples_split = 40, max_depth = 12)
    clf.fit(X_train, y_train)
    filename = '/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output/finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    return clf


def predict(X_test, y_test, X_train, y_train, trained_model = 'yes'):
    if trained_model == 'yes':
        loaded_model = pickle.load(open('/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output/finalized_model.sav', 'rb'))
        result = loaded_model.score(X_test, y_test)
        print(f"Model's validation accuracy: {result:.5f}")
        predictions = loaded_model.predict(X_test)
        return predictions

    if trained_model == 'no':
        print("Retraining the model")
        model = train(X_train, y_train)
        result = model.score(X_test, y_test)
        print(f"Model's validation accuracy: {result:.5f}")
        predictions = model.predict(X_test)
        return predictions
