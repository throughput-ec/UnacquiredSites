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


# Assigning the REGEX for dd and dms coordinates

dms_regex = r"([-]?\d{1,3}[°|′|\'|,]{0,3}\d{1,2}[,|′|\']{1,3}\d{0,2}[,|′|\']{1,4}[NESWnesw]?[\s|,|\']+?[-]?\d{1,3}[°|,|′|\']+\d{1,2}[,|′|\']+\d{0,2}[,|′|\'][,|′|\']{0,4}[NESWnesw]?)"
dd_regex =  r"([-]?\d{1,3}\.\d{1,}[,]?[NESWnesw][\s|,|\']+?[-]?\d{1,3}\.\d{1,}[,]?[NESWnesw])"

# Add columns to dataframe for the dms and dd REGEX
nlp_sentences['words_as_string'] = nlp_sentences['words'].apply(lambda x: ','.join(map(str, x)))
nlp_sentences['dms_regex'] = nlp_sentences['words_as_string'].str.findall(dms_regex)
nlp_sentences['dd_regex'] = nlp_sentences['words_as_string'].str.findall(dd_regex)


path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output'
output_file = os.path.join(path,'nlp_sentences_df.csv')
nlp_sentences.to_csv(output_file, sep='\t', index = False)
