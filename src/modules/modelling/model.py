import pandas as pd
import numpy as np

# Loading libraries for modeling
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, recall_score

import time
import pickle

import argparse
import sys
import os

import cProfile, pstats, io
#warnings.filterwarnings("ignore")

'''USAGE
python3 src/modules/modelling/model.py \
--input_file='output/preprocessed_data/preprocessed_sentences.tsv' \
--eda_file='yes'
'''

in_file_name = r'output/preprocessed_data/preprocessed_sentences.tsv'
out_file = r'output/predictions/predictions_train.tsv'
eda_file = r'output/eda/probabilities_percentiles_df.tsv'

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_file', type=str, default=in_file_name,
                        help='Directory where your input data is.')

    parser.add_argument('--output_file', type=str, default=out_file,
                        help='Directory where your input data is.')

    parser.add_argument('--eda_file', type=str, default='no',
                        help='Do EDA files yes/no.')

    args = parser.parse_args()


    X_train, y_train, dataframe = prepare_data(file = args.input_file)
    print("Using CountVectorizer to preprocess data...")

    # Start training
    clf = train(X_train, y_train)
    print("Training model...")

    y_pred, y_proba = predictions(X_train, y_train)
    print("Completed metrics")

    guessed_label = pd.DataFrame(y_pred)
    actual_label = pd.DataFrame(y_train)
    predicted_proba = pd.DataFrame(y_proba)
    actual_label = actual_label.reset_index()

    original_sentence = pd.DataFrame(dataframe[['gddid', 'title', 'sentid','sentence', 'found_lat', 'latnorth', 'found_long', 'longeast']])
    original_sentence = original_sentence.reset_index()

    prediction_comp = guessed_label.join(actual_label)
    prediction_comp = prediction_comp.drop(columns=['index'])
    prediction_comp.columns = ['predicted_label'] + prediction_comp.columns.tolist()[1:]

    prediction_comp = predicted_proba.join(prediction_comp)
    prediction_comp.columns = ['prediction_proba'] + prediction_comp.columns.tolist()[1:]

    prediction_comp = prediction_comp.join(original_sentence)
    prediction_comp = prediction_comp.drop(columns=['index'])
    prediction_comp = prediction_comp.rename(columns={'0':'predicted_proba'})

    prediction_comp['Train/Pred'] = 'Train'
    prediction_comp = prediction_comp[['gddid', 'title', 'sentid', 'sentence', 'predicted_label', 'prediction_proba', 'true_label', 'found_lat', 'latnorth', 'found_long', 'longeast', 'Train/Pred']]
    output_file = os.path.join(args.output_file)
    prediction_comp.to_csv(output_file, sep='\t', index = False)
    print(f"Saving validation - prediction comparison dataframe in: {output_file}")

    ## Getting a df with percentiles.
    if args.eda_file == 'yes':
        print('Saving percentiles and metrics analysis in EDA folder')
        percentiles = pd.DataFrame(prediction_comp['prediction_proba'])

        bins = pd.cut(percentiles['prediction_proba'], [0.0, 0.125, 0.25, 0.50, 0.75, 1.0])
        df = percentiles.groupby(bins)['prediction_proba'].agg(['count'])
        df = df.reset_index()
        df['perc'] = round(df['count']/df['count'].sum(),5)*100

        df.to_csv(r'output/eda/comparison_percentiles.tsv', sep='\t', index = False)

        sys.stdout = open("output/eda/train_metrics.txt", "w")
        print('NB-conf. matrix-from trained: \n\n', confusion_matrix(y_train, y_pred))
        print('NB-recall-from trained:', recall_score(y_train, y_pred))
        print('Check metrics milestones for test set in Notebooks')
        sys.stdout.close()


def prepare_data(file = in_file_name):
    input_file = file

    df = pd.read_csv(input_file, sep='\t')
    print("Did not use file with validated coordinates")

    df['true_label'] = ((df['found_lat'].apply(len) > 2) & (df['found_long'].apply(len) > 2 ))

    # Map True to One and False to Zero
    df['true_label'] = df['true_label'].astype(int)

    # NLP Bag of Words
    vec = CountVectorizer(min_df=2)

    # Fit and transform training
    X_train = vec.fit_transform(df['nltk'].fillna(' '))
    y_train = df['true_label']

    vec_model = 'output/count_vec_model.sav'
    print('Trained CountVectorizer')
    pickle.dump(vec, open(vec_model, 'wb'))

    return X_train, y_train, df


def train(X_train, y_train):
    clf = MultinomialNB()
    #clf = DecisionTreeClassifier(min_samples_split = 40, max_depth = 12) - first model
    clf.fit(X_train, y_train)
    filename = 'output/NB_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    print('Trained NaiveBayes')
    return clf

def predictions(X_train, y_train, eda = 'yes'):
    loaded_model = pickle.load(open('output/NB_model.sav', 'rb'))
    training_acc = loaded_model.score(X_train, y_train)
    print(f"The model's training accuracy was of: {training_acc:.5f}")
    y_pred = loaded_model.predict(X_train)
    y_proba = loaded_model.predict_proba(X_train)[:,1]

    return y_pred, y_proba

# Remove docstring for profiling
'''
pr = cProfile.Profile()
pr.enable()

my_result = main()

pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats()

with open('output/profiling/profiling_model.txt', 'w+') as f:
    f.write(s.getvalue())
'''

if __name__ == '__main__':
    main()
