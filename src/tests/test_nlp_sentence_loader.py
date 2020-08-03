import pandas as pd
import src.modules.preprocessing.nlp_sentence_loader as nl


def test_preprocessed_sentences_sql():
    '''
    preprocessed_sentences_sql()
    Load data from SQL
    '''
    data = nl.preprocessed_sentences_sql(query = '''SELECT * FROM sentences;''')
    assert isinstance(data, pd.DataFrame)
