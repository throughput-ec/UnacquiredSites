# File reading
import pandas as pd
import psycopg2
import ast

# For script use imports as:
import utils
import config as config

# NLP Modules
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

file = r'data/sentences_nlp352'
def preprocessed_sentences_tsv(path = file):
    nlp_sentences = pd.read_csv(path, sep='\t', names = ['gddid', 'sentid', 'wordidx', 'words', 'part_of_speech', 'special_class',
               'lemmas', 'word_type', 'word_modified'], usecols = ['gddid', 'sentid', 'words'])
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
    # Sentences - not words.
    nlp_sentences['sentence'] = nlp_sentences['words'].apply(lambda x: ','.join(map(str, x)))

    # REGEX Values
    nlp_sentences = utils.find_regex(nlp_sentences, find_val = 'dms_regex',\
                                search_col = 'sentence', new_col_name = 'dms_re')
    nlp_sentences = utils.find_regex(nlp_sentences, find_val = 'dd_regex',\
                                search_col = 'sentence', new_col_name = 'dd_re')
    nlp_sentences = utils.find_regex(nlp_sentences, find_val = 'digits_regex',\
                                search_col = 'sentence', new_col_name = 'digits_re')

    # NLP Taks
    stop = stopwords.words('english')
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    stemmer = SnowballStemmer("english")

    nlp_sentences['nltk'] = nlp_sentences.apply(lambda row: tokenizer.tokenize(row['sentence']), axis=1)
    nlp_sentences['nltk']=nlp_sentences['nltk'].apply(lambda x: [item for item in x if item not in stop])
    nlp_sentences['nltk']=nlp_sentences['nltk'].apply(lambda x: [stemmer.stem(y) for y in x])
    nlp_sentences = nlp_sentences[['gddid', 'sentid', 'sentence', 'nltk', 'dms_re', 'dd_re', 'digits_re']]
    
    return nlp_sentences

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
        nlp_sentences['words_as_string'] = nlp_sentences['words'].apply(lambda x: ','.join(map(str, x)))

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

        nlp_sentences = utils.find_re(nlp_sentences, find_val = 'dms_regex',\
         search_col = 'words_as_string', new_col_name = 'dms_regex')
        nlp_sentences = utils.find_re(nlp_sentences, find_val = 'dd_regex',\
         search_col = 'words_as_string', new_col_name = 'dd_regex')
        nlp_sentences = utils.find_re(nlp_sentences, find_val = 'digits_regex',\
         search_col = 'words_as_string', new_col_name = 'digits_regex')

        # Format words to lowercase
        nlp_sentences['words_l'] = nlp_sentences['words']\
            .astype(str).str.lower().transform(ast.literal_eval)

        return nlp_sentences

    except Exception as e:
        print(e)
        print('No SQL found. If you have a tsv file, try using preprocessed_sentences_tsv().')
