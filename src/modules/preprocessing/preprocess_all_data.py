import src.modules.preprocessing.nlp_sentence_loader as sentence_loader
import src.modules.preprocessing.bibliography_loader as bib_loader
import src.modules.preprocessing.add_regex_degrees as ard
import src.modules.preprocessing.neotoma_loader as nl


def get_all_datasets():
    nlp_sentences = sentence_loader.preprocessed_sentences_sql()
    bibliography = bib_loader.preprocessed_bibliography()
    neotoma = nl.neotoma_loader()
    neotoma_joined_df = nl.grouped_coords_df(neotoma)

    return nlp_sentences, bibliography, neotoma, neotoma_joined_df

def get_nlp_bib_neotoma(nlp_sentences, bibliography, neotoma_joined_df):
    nlp_bib = nlp_sentences.merge(bibliography, on = '_gddid')
    nlp_bib_neotoma = nlp_bib.merge(neotoma_joined_df, on = 'doi', how = 'left')
    return nlp_bib, nlp_bib_neotoma