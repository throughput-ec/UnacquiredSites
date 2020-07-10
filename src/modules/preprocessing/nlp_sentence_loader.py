import pandas as pd
import psycopg2
import re
import ast
import src.modules.preprocessing.add_regex_degrees as ard
#src.modules.preprocessing.
# Load Postgres Server
import src.modules.preprocessing.config as config

# Connect to PostgreSQL server from terminal:
# pg_ctl -D PSQL_Data -l logfile start
def preprocessed_sentences_sql(query = '''SELECT * FROM sentences;'''):
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
        print('Data obtained from PostgreSQL')

        # Add REGEX columns to data.
        nlp_sentences = ard.convert_words_to_string(nlp_sentences, col_to_convert = 'words', new_col_name = 'words_as_string')

        # REGEX Values

        nlp_sentnences = ard.find_re(nlp_sentences, find_val = 'dms_regex', search_col = 'words_as_string', new_col_name = 'dms_regex')
        nlp_sentnences = ard.find_re(nlp_sentences, find_val = 'dd_regex', search_col = 'words_as_string', new_col_name = 'dd_regex')
        nlp_sentnences = ard.find_re(nlp_sentences, find_val = 'digits_regex', search_col = 'words_as_string', new_col_name = 'digits_regex')

        # Format words to lowercase
        nlp_sentences['words_l']  = nlp_sentences['words'].astype(str).str.lower().transform(ast.literal_eval)

        return nlp_sentences

    except:
        print('No SQL found. Try a different data source')


# If no SQL db, load from a file
def preprocessed_sentences_csv(path = "../Do_not_commit_data/sentences_nlp352"):
    """
    Loads and formats NLP sentences CSV file and converts to a dataframe

    Parameters
    ----------
    path : string
        Path where csv with NLP Sentences can be found

    Returns
    -------
    nlp_sentences: pd.DataFrame
        pd.DataFrame with all NLP Sentences database information
    """
    header_list = ["_gddid", "sentid", "wordidx", "words", "part_of_speech", "special_class",
                   "lemmas", "word_type", "word_modified"]
    nlp_sentences = pd.read_csv(path, sep='\t', names = header_list)
    nlp_sentences = nlp_sentences.replace('"', '', regex = True)\
                                 .replace('\{', '', regex = True)\
                                 .replace('}', '', regex = True)\
                                 .replace(',', ',', regex = True)
    nlp_sentences['wordidx']= nlp_sentences['wordidx'].str.split(",")
    nlp_sentences['words']= nlp_sentences['words'].str.split(",")
    nlp_sentences['poses']= nlp_sentences['poses'].str.split(",")
    nlp_sentences['ners']= nlp_sentences['ners'].str.split(",")
    nlp_sentences['lemmas']= nlp_sentences['lemmas'].str.split(",")
    nlp_sentences['dep_paths']= nlp_sentences['dep_paths'].str.split(",")
    nlp_sentences['dep_parents']= nlp_sentences['dep_parents'].str.split(",")

    # Add REGEX columns to data.
    nlp_sentences = ard.convert_words_to_string(nlp_sentences, col_to_convert = 'words', new_col_name = 'words_as_string')
    nlp_sentences = ard.add_dms_re(nlp_sentences, search_col = 'words_as_string', new_col_name = 'dms_regex')
    nlp_sentences = ard.add_dd_re(nlp_sentences, search_col = 'words_as_string', new_col_name = 'dd_regex')
    nlp_sentences = ard.find_digits_from_words(nlp_sentences, search_col = 'words_as_string', new_col_name = 'digits_from_words')
    nlp_sentences['words_l']  = nlp_sentences['words'].astype(str).str.lower().transform(ast.literal_eval)
    return nlp_sentences
    print('Data obtained from text file')
