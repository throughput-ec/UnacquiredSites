# For script use imports as:
import sentence_loader as sl
import bibliography_loader as bl
import neotoma_loader as nl
import utils as utils
import eda_creator as ec

import argparse
import os
import cProfile
import pstats
import io
#Swarnings.filterwarnings("ignore")

'''
USAGE
python3 src/preprocess_all_data.py \
--output_name='output/for_model/preprocessed_sentences.tsv' \
--bib_file='data/bibjson' \
--neotoma_file='data/data-1590729612420.csv' \
--create_eda='yes'
'''

file = r'output/for_model/preprocessed_sentences.tsv'
nlp_file=r'data/sentences_nlp352'
bib_file = r'data/bibjson'
neotoma_file = r'data/data-1590729612420.csv'
tsv_or_sql = 'tsv'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nlp_file', type=str, default=nlp_file,
                        help='Directory with NLP CSV')
    parser.add_argument('--bib_file', type=str, default=bib_file,
                        help='Directory where bibliography json file is.')
    parser.add_argument('--neotoma_file', type=str, default=neotoma_file,
                        help='Directory with Neotmas CSV.')
    parser.add_argument('--output_name', type=str, default=file,
                        help='Path + Name of the file as tsv.')
    parser.add_argument('--create_eda', type=str, default='no',
                        help='Use train model or no. Options: yes/no')
    parser.add_argument('--tsv_or_sql', type=str, default='tsv',
                        help='Use a sql base or csv base')
    args = parser.parse_args()

    print("Loading datasets")

    nlp_sentences, bibliography, neotoma, neotoma_summary = get_all_datasets(bib_path=args.bib_file,
                                                                             neotoma_path=args.neotoma_file,
                                                                             nlp_path=args.nlp_file,
                                                                             tsv_or_sql=args.tsv_or_sql)


    nlp_bib, preprocessed_df = get_nlp_bib_neotoma(nlp_sentences,
                                                   bibliography,
                                                   neotoma_summary)

    print("...preprocessing data... please wait...")

    preprocessed_df = utils.find_intersections(preprocessed_df,
                                             cols_to_intersect=['digits_re',
                                                                'longeast'],
                                             new_col_name='found_long')
    preprocessed_df = utils.find_intersections(preprocessed_df,
                                             cols_to_intersect=['digits_re',
                                                                'latnorth'],
                                             new_col_name='found_lat')
    preprocessed_df = utils.find_intersections(preprocessed_df,
                                             cols_to_intersect=['sentence',
                                                                'sitenames_l'],
                                             new_col_name='found_sites')

    preprocessed_df_for_model = preprocessed_df[['gddid',
                                                 'sentid',
                                                 'title',
                                                 'sentence',
                                                 'nltk',
                                                 'digits_re',
                                                 'found_lat',
                                                 'latnorth',
                                                 'found_long',
                                                 'longeast']]

    output_file = os.path.join(args.output_name)
    preprocessed_df_for_model.to_csv(output_file, sep='\t', index=False)

    print(f"You can find the preprocessed data in: {args.output_name}")

    if args.create_eda == 'yes':
        print("Creating EDA files")
        ec.not_in_neotoma(df = preprocessed_df, df2 = bibliography)
        ec.sentences_w_coords_int(preprocessed_df)
        ec.articles_wo_coords(preprocessed_df, bibliography, neotoma_summary)
        ec.sentences_w_site_int(preprocessed_df)
        ec.articles_wo_sites(preprocessed_df, bibliography, neotoma_summary)

    if args.create_eda == 'no':
        print("No EDA files was created.")



def get_all_datasets(nlp_path=nlp_file, bib_path=bib_file, neotoma_path=neotoma_file, tsv_or_sql='tsv'):
    """
    Runs all data creator functions to get four main datasets

    Parameters
    ----------

    Returns
    -------
    nlp_sentences : pd.DataFrame
        pd.DataFrame with all NLP Sentences database information
    bibliography : pd.DataFrame
        pd.DataFrame with all Bibliography database information
    neotoma : pd.DataFrame
        pd.DataFrame with all Neotoma database information
    neotoma_summary : pd.DataFrame
        pd.DataFrame with all neotoma_summary database information
    """

    if tsv_or_sql=='sql':
        nlp_sentences = sl.preprocessed_sentences_sql()
    if tsv_or_sql=='tsv':
        print("loading from tsv file")
        nlp_sentences = sl.preprocessed_sentences_tsv(path=nlp_path)

    bibliography = bl.preprocessed_bibliography(path=bib_path)
    neotoma = nl.neotoma_loader(file=neotoma_path)
    neotoma_summary = nl.grouped_coords_df(neotoma)

    return nlp_sentences, bibliography, neotoma, neotoma_summary


def get_nlp_bib_neotoma(nlp_sentences, bibliography, neotoma_summary):
    """
    Uses all main datasets to create preprocessed_df dataframe

    Parameters
    ----------
    nlp_sentences : pd.DataFrame
        pd.DataFrame with all NLP Sentences database information
    bibliography : pd.DataFrame
        pd.DataFrame with all Bibliography database information
    neotoma_summary : pd.DataFrame
        pd.DataFrame with all neotoma_summary database information

    Returns
    -------
    nlp_bib : pd.DataFrame
        pd.DataFrame with summarized merged nlp sentences and bibliography
        information
    preprocessed_df : pd.DataFrame
        pd.DataFrame with summarized NLP, Bibliography and Neotoma database
        information
    """
    nlp_bib = nlp_sentences.merge(bibliography, on='gddid')
    preprocessed_df = nlp_bib.merge(neotoma_summary, on='doi')
    return nlp_bib, preprocessed_df

# Do it once to do your profiling. Then comment this code chunk.
#pr = cProfile.Profile()
#pr.enable()

#my_result = main()

#pr.disable()
#s = io.StringIO()
#ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
#ps.print_stats()

#with open('src/output/profiling/profiling_preprocess_data.txt', 'w+') as f:
#    f.write(s.getvalue())

if __name__ == '__main__':
    main()
