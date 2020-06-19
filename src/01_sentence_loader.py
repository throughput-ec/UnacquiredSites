import numpy as np
import pandas as pd
import csv
import psycopg2
import re
import ast
import os

# Load Postgres Server
from config import config

# Connect to PostgreSQL server from terminal:
# pg_ctl -D PSQL_Data -l logfile start


try:
    params = config()
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**params)
    # Create a new cursor
    cur = conn.cursor()
    nlp_sentences = pd.read_sql_query('''SELECT * FROM sentences;''', conn)
    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()
    print('Data obtained from PostgreSQL')

# If no SQL db, load from a file
except:
    header_list = ["_gddid", "sentid", "wordidx", "words", "part_of_speech", "special_class",
               "lemmas", "word_type", "word_modified"]
    nlp_sentences = pd.read_csv("../Do_not_commit_data/sentences_nlp352", sep='\t', names = header_list)
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
    print('Data obtained from text file')

path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output'
output_file = os.path.join(path,'nlp_sentences_df.csv')
nlp_sentences.to_csv(output_file, index = False)
