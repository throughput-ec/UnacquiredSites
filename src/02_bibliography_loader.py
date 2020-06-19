import numpy as np
import pandas as pd
import csv
import psycopg2
import re
import ast
import os

# Load Postgres Server
from config import config

import json


with open('../Do_not_commit_data/bibjson', 'r') as f:
    bib_dict = json.load(f)


# Normalizing data so that we have access to the 'identifier'

# TODO Load into SQL server and connect through SQL
bibliography = pd.io.json.json_normalize(bib_dict,'identifier',['publisher', 'title', ['journal','name', 'name'], ['author'], 'year', 'number', 'volumne', ['link'], '_gddid', 'type', 'pages'], record_prefix='_', errors='ignore')

bibliography['link'] = bibliography['link'].astype(str)

url = bibliography['link'].str.split(", ", expand = True)

bibliography['link_url'] = url[0]
bibliography['link_type'] = url[1]

bibliography['link_url'] = bibliography['link_url'].replace("\[{'url': '", "", regex = True)\
                                                   .replace("'", "", regex = True)

bibliography['link_type'] = bibliography['link_type'].replace("'type': '", "", regex = True)\
                                                     .replace("'}]", "", regex = True)

bibliography['author'] = bibliography['author'].astype(str)
bibliography['author'] = bibliography['author'].replace("\[{'name': '", "", regex = True)\
                                               .replace("{'name': '", "", regex = True)\
                                               .replace("'},", ";", regex = True)\
                                               .replace("'}]", "", regex = True)
bibliography = bibliography[['_type', '_id', 'publisher', 'title', 'journal.name.name',	'author', 'year', 'number', 'volumne', '_gddid', 'type', 'pages', 'link_url', 'link_type']]

path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output'
output_file = os.path.join(path,'bibliography.csv')
bibliography.to_csv(output_file, index = False)
