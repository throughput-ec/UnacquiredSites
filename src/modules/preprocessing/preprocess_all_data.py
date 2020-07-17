import src.modules.preprocessing.nlp_sentence_loader as sentence_loader
import src.modules.preprocessing.bibliography_loader as bib_loader
import src.modules.preprocessing.neotoma_loader as nl


def get_all_datasets():
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
    nlp_sentences = sentence_loader.preprocessed_sentences_sql()
    bibliography = bib_loader.preprocessed_bibliography()
    neotoma = nl.neotoma_loader()
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
        pd.DataFrame with summarized merged nlp sentences and
        bibliography information
    nlp_bib_neotoma : pd.DataFrame
        pd.DataFrame with summarized NLP, Bibliography and Neotoma
        database information
    """
    nlp_bib = nlp_sentences.merge(bibliography, on='_gddid')
    nlp_bib_neotoma = nlp_bib.merge(neotoma_joined_df, on='doi', how='left')
    return nlp_bib, nlp_bib_neotoma
