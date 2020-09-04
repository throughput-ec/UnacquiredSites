
import argparse
import os
import cProfile
import pstats
import io
import utils as ard
import bibliography_loader as bl

file = r'data/for_prediction'
bibliography = r'data/bibjson2'
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
    biblio = bl.preprocessed_bibliography(bibliography)
    nlp_bib = nlp_sentences.merge(bibliography, on='_gddid')

    y_pred, y_proba = predict(data_test = nlp_bib)

    guessed_label = pd.DataFrame(y_pred)
    predicted_proba = pd.DataFrame(y_proba)

    original_sentence = pd.DataFrame(nlp_bib[['_gddid', 'title', 'sentid','words_as_string']])
    original_sentence = original_sentence.reset_index()

    test_pred_comp = guessed_label.join(predicted_proba)
    test_pred_comp = test_pred_comp.drop(columns=['index'])
    test_pred_comp.columns = ['predicted_label'] + test_pred_comp.columns.tolist()[1:]

    test_pred_comp = test_pred_comp.join(original_sentence)
    test_pred_comp = test_pred_comp.drop(columns=['index'])
    test_pred_comp = test_pred_comp.rename(columns={'0':'predicted_proba', 'words_as_string':'sentence'})

    output_file = os.path.join(args.output_file)
    test_pred_comp.to_csv(output_file, sep='\t', index = False)
    print(f"Saving predictions: {output_file}")


def preprocessed_sentences_csv(path = file):
    header_list = ["_gddid", "sentid", "wordidx", "words", "part_of_speech", "special_class",
               "lemmas", "word_type", "word_modified"]
    nlp_sentences = pd.read_csv(path, sep='\t', names = header_list)
    nlp_sentences = nlp_sentences['_gddid', 'sentid', 'words']
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

    # Add REGEX columns to data.
    nlp_sentences = ard.convert_words_to_string(nlp_sentences, col_to_convert = 'words', new_col_name = 'words_as_string')
    return nlp_sentences

def predict(data_test):
    X_test = vec.transform(data_test['words_as_string'].fillna(' '))
    loaded_model = pickle.load(open('src/output/finalized_model.sav', 'rb'))
    y_pred = loaded_model.predict(X_test)
    y_proba = loaded_model.predict_proba(X_test)[:,1]
    return y_pred, y_proba
