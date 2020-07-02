import src.modules.preprocessing.nlp_sentence_loader as sentence_loader
import src.modules.preprocessing.bibliography_loader as bib_loader
import src.modules.preprocessing.add_regex_degrees as ard
import src.modules.preprocessing.neotoma_loader as nl


def get_all_datasets():
    nlp_sentences = sentence_loader.preprocessed_sentences_sql()
    bibliography = bib_loader.preprocessed_bibliography()
    neotoma = nl.neotoma_loader()

    return nlp_sentences, bibliography, neotoma
