# For script use imports as:
import nlp_sentence_loader as sentence_loader
import bibliography_loader as bib_loader
import utils as ard
import neotoma_loader as nl
import eda_creator as ec

# For Jupyter
#import src.modules.preprocessing.nlp_sentence_loader as sentence_loader
#import src.modules.preprocessing.bibliography_loader as bib_loader
#import src.modules.preprocessing.utils as ard
#import src.modules.preprocessing.neotoma_loader as nl
import argparse
import os
import cProfile
import pstats
import io

# USAGE
# python3 src/preprocess_all_data.py \
# --output_name='output/for_model/preprocessed_sentences.tsv' \
# --bib_file='data/bibjson' \
# --neotoma_file='data/data-1590729612420.csv' \
# --create_eda='yes'

file = r'output/for_model/preprocessed_sentences.tsv'
bib_file = r'data/bibjson'
neotoma_file = r'data/data-1590729612420.csv'
nlp_file=r'data/sentences_nlp352'
tsv_or_sql = 'tsv'


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--output_name', type=str, default=file,
                        help='Path + Name of the file as tsv.')
    parser.add_argument('--bib_file', type=str, default=bib_file,
                        help='Directory where bibliography json file is.')
    parser.add_argument('--neotoma_file', type=str, default=neotoma_file,
                        help='Directory with Neotmas CSV.')

    parser.add_argument('--nlp_file', type=str, default=nlp_file,
                        help='Directory with NLP CSV')


    parser.add_argument('--create_eda', type=str, default='no',
                        help='Use train model or no. Options: yes/no')

    parser.add_argument('--tsv_or_sql', type=str, default='tsv',
                        help='Use a sql base or csv base')
    args = parser.parse_args()

    print("Loading all datasets")

    nlp_sentences, bibliography, neotoma, neotoma_joined_df = get_all_datasets(bib_path=args.bib_file,
                                                                               neotoma_path=args.neotoma_file,
                                                                               nlp_path=args.nlp_file,
                                                                               tsv_or_sql=args.tsv_or_sql)


    nlp_bib, nlp_bib_neotoma = get_nlp_bib_neotoma(nlp_sentences,
                                                   bibliography,
                                                   neotoma_joined_df)

    print("...preprocessing data... please wait...")

    nlp_bib_neotoma = ard.find_intersections(nlp_bib_neotoma,
                                             cols_to_intersect=['digits_regex',
                                                                'longeast'],
                                             new_col_name='found_long')
    nlp_bib_neotoma = ard.find_intersections(nlp_bib_neotoma,
                                             cols_to_intersect=['digits_regex',
                                                                'latnorth'],
                                             new_col_name='found_lat')
    nlp_bib_neotoma = ard.find_intersections(nlp_bib_neotoma,
                                             cols_to_intersect=['words_l',
                                                                'sitenames_l'],
                                             new_col_name='found_sites')

    nlp_bib_neotoma_for_model = nlp_bib_neotoma[['_gddid',
                                                 'title',
                                                 'digits_regex',
                                                 'sentid',
                                                 'words',
                                                 'words_as_string',
                                                 'link_url',
                                                 'found_lat',
                                                 'latnorth',
                                                 'found_long',
                                                 'longeast',
                                                 'found_sites']]



    output_file = os.path.join(args.output_name)
    nlp_bib_neotoma_for_model.to_csv(output_file, sep='\t', index=False)

    print(f"You can find the preprocessed data in: {args.output_name}")

    if args.create_eda == 'yes':
        print("Creating EDA files")
        ec.not_in_neotoma(df = nlp_bib_neotoma, df2 = bibliography)
        ec.sentences_w_coords_int(nlp_bib_neotoma)
        ec.articles_wo_coords(nlp_bib_neotoma, bibliography, neotoma_joined_df)
        ec.sentences_w_site_int(nlp_bib_neotoma)
        ec.articles_wo_sites(nlp_bib_neotoma, bibliography, neotoma_joined_df)

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
    neotoma_joined_df : pd.DataFrame
        pd.DataFrame with all Neotoma_Joined_DF database information
    """

    if tsv_or_sql=='sql':
        nlp_sentences = sentence_loader.preprocessed_sentences_sql()
    if tsv_or_sql=='tsv':
        print("loading from tsv file")
        nlp_sentences = sentence_loader.preprocessed_sentences_tsv(path=nlp_path)

    bibliography = bib_loader.preprocessed_bibliography(path=bib_path)
    neotoma = nl.neotoma_loader(file=neotoma_path)
    neotoma_joined_df = nl.grouped_coords_df(neotoma)

    return nlp_sentences, bibliography, neotoma, neotoma_joined_df


def get_nlp_bib_neotoma(nlp_sentences, bibliography, neotoma_joined_df):
    """
    Uses all main datasets to create NLP_BIB_NEOTOMA dataframe

    Parameters
    ----------
    nlp_sentences : pd.DataFrame
        pd.DataFrame with all NLP Sentences database information
    bibliography : pd.DataFrame
        pd.DataFrame with all Bibliography database information
    neotoma_joined_df : pd.DataFrame
        pd.DataFrame with all Neotoma_Joined_DF database information

    Returns
    -------
    nlp_bib : pd.DataFrame
        pd.DataFrame with summarized merged nlp sentences and bibliography
        information
    nlp_bib_neotoma : pd.DataFrame
        pd.DataFrame with summarized NLP, Bibliography and Neotoma database
        information
    """
    nlp_bib = nlp_sentences.merge(bibliography, on='_gddid')
    nlp_bib_neotoma = nlp_bib.merge(neotoma_joined_df, on='doi')
    return nlp_bib, nlp_bib_neotoma

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
