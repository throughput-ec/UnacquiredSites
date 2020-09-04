import pandas as pd
import psycopg2
import ast

# For script use imports as:
import utils as ard
import config as config

# For Jupyter notebook change imports to
#import src.modules.preprocessing.config as config
#import src.modules.preprocessing.utils as ard


# Connect to PostgreSQL server from terminal:
# pg_ctl -D PSQL_Data -l logfile start
def preprocessed_sentences_sql(query='''SELECT * FROM sentences2;'''):
    """
    Loads and formats NLP sentences SQL file and converts to a dataframe

    Parameters
    ----------
    query : string
        SQL query to pull NLP sentence relational database

    Returns
    -------
    nlp_sentences: pd.DataFrame
        pd.DataFrame with all NLP Sentences database information
    """

    try:
        params = config.config()
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()

        nlp_sentences = pd.read_sql_query(query, conn)
        # Close the cursor and connection to so the server can allocate
        # bandwidth to other requests
        cur.close()
        conn.close()

        # Add REGEX columns to data.
        nlp_sentences = ard\
            .convert_words_to_string(nlp_sentences,
                                     col_to_convert='words',
                                     new_col_name='words_as_string')

        nlp_sentences['words_as_string'] = nlp_sentences['words_as_string']\
            .replace(r'\W{4,}', '', regex=True)\
            .replace(',,,', 'comma_sym', regex=True)\
            .replace(',', ' ', regex=True)\
            .replace('comma_sym', ', ', regex=True)\
            .replace('-LRB- ', '(', regex=True)\
            .replace('LRB', '(', regex=True)\
            .replace(' -RRB-', r')', regex=True)\
            .replace('RRB', r')', regex=True)\
            .replace('-RRB', r')', regex=True)

        # REGEX Values

        nlp_sentences = ard.find_re(nlp_sentences, find_val = 'dms_regex',\
         search_col = 'words_as_string', new_col_name = 'dms_regex')
        nlp_sentences = ard.find_re(nlp_sentences, find_val = 'dd_regex',\
         search_col = 'words_as_string', new_col_name = 'dd_regex')
        nlp_sentences = ard.find_re(nlp_sentences, find_val = 'digits_regex',\
         search_col = 'words_as_string', new_col_name = 'digits_regex')

        # Format words to lowercase
        nlp_sentences['words_l'] = nlp_sentences['words']\
            .astype(str).str.lower().transform(ast.literal_eval)

        return nlp_sentences

    except Exception as e:
        print(e)
        print('No SQL found. Try a different data source')
