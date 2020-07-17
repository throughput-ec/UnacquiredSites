import pandas as pd
import json


def preprocessed_bibliography(path):
    """
    Loads and formats bibliography json file and converts to a dataframe

    Parameters
    ----------
    path : string
        Path where the bibliography database is stored.

    Returns
    -------
    bibliography: pd.DataFrame
        pd.DataFrame with all bibliography information
    """
    with open(path, 'r') as f:
        bib_dict = json.load(f)
    # Normalizing data so that we have access to the 'identifier'

    # TODO Load into SQL server and connect through SQL
    bibliography = pd.io.json.json_normalize(bib_dict,
                                             'identifier',
                                             ['publisher', 'title',
                                              ['journal', 'name', 'name'],
                                              ['author'], 'year', 'number',
                                              'volumne', ['link'], '_gddid',
                                              'type', 'pages'],
                                             record_prefix='_',
                                             errors='ignore')

    bibliography['link'] = bibliography['link'].astype(str)

    url = bibliography['link'].str.split(", ", expand=True)

    bibliography['link_url'] = url[0]
    bibliography['link_type'] = url[1]

    bibliography['link_url'] = bibliography['link_url']\
        .replace(r"\[{'url': '", "", regex=True)\
        .replace(r"'", "", regex=True)

    bibliography['link_type'] = bibliography['link_type']\
        .replace(r"'type': '", "", regex=True)\
        .replace("'}]", "", regex=True)

    bibliography['author'] = bibliography['author'].astype(str)
    bibliography['author'] = bibliography['author']\
        .replace(r"\[{'name': '", "", regex=True)\
        .replace(r"{'name': '", "", regex=True)\
        .replace("'},", ";", regex=True)\
        .replace("'}]", "", regex=True)

    bibliography = bibliography[['_type', '_id', 'publisher',
                                 'title', 'journal.name.name',
                                 'author', 'year', 'number', 'volumne',
                                 '_gddid', 'type', 'pages',
                                 'link_url', 'link_type']]

    bibliography = bibliography.rename(columns={'_id': 'doi'})
    return bibliography
