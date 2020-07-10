import pandas as pd
import os
import ast
from nltk.tokenize import word_tokenize


def neotoma_loader(file = "/Users/seiryu8808/Desktop/UWinsc/Github/Do_not_commit_data/data-1590729612420.csv"):
    """
    Loads and formats neotoma database file and converts to a dataframe

    Parameters
    ----------
    file : string
        Path where the NEOTOMA database is stored.

    Returns
    -------
    neotoma: pd.DataFrame
        pd.DataFrame with all Neotoma information
    """
    neotoma = pd.read_csv(file)
    neotoma = neotoma[['siteid', 'sitename', 'longitudeeast', 'latitudenorth', 'longitudewest', 'latitudesouth', 'sitedescription', 'doi']]
    return neotoma

def format_coords(df, col_to_convert, col_new_name):
    """
    Takes col_to_convert and creates a list of a set of strings that contain coordinates in an integer form.

    Parameters
    ----------
    df : df
        pd.DataFrame that contains Neotoma information.
    col_to_convert :  string
        Name of column of df. This column has latitude and longitude coordinates
    col_new_name : string
        Name of new column of df.

    Returns
    -------
    df: pd.DataFrame
        pd.DataFrame with new column `col_new_name` which contains a list of unique positive integer coordinates.
    """
    df[col_new_name] = df[col_to_convert].apply(lambda x: [int(abs(i)) for i in x])\
                                         .apply(lambda x: [str(i) for i in x])\
                                         .replace('-', '', regex = True)\
                                         .apply(lambda x: list(set(x)))
    return df

def format_sitenames(df, col_to_convert, col_new_name):
    """
    Takes col_to_convert and creates a list of a set of strings that contain unique sitenames in lowercase.

    Parameters
    ----------
    df : df
        pd.DataFrame that contains Neotoma information
    col_to_convert :  string
        Name of column of df. This column has name of sitenames
    col_new_name : string
        Name of new column of df.

    Returns
    -------
    df: pd.DataFrame
        pd.DataFrame with new column `col_new_name` which contains a list of unique lower cased sitenames.
    """
    df[col_new_name] = df[col_to_convert].astype(str).str.lower().transform(ast.literal_eval)\
                                         .apply(lambda x: [word_tokenize(i) for i in x])\
                                         .apply(lambda l: [item for sublist in l for item in sublist])\
                                         .apply(lambda x: list(set(x)))
    return df


def grouped_coords_df(df, group_by_var = 'doi'):
    """
    Takes a dataframe and groups it by a key entry (document ID) summarizing sitenames and coordinates per document ID

    Parameters
    ----------
    df : string
        pd.DataFrame that contains Neotoma information
    group_by_var :  string
        Key that will help group and summarize the Neotoma Database

    Returns
    -------
    df: pd.DataFrame
        pd.DataFrame with summarized coordinates and sitenames
    """
    by_var = df.groupby(group_by_var)
    df_sitenames = by_var.apply(lambda x: list(x['sitename']))
    df_siteid = by_var.apply(lambda x: list(x['siteid']))
    df_longeast = by_var.apply(lambda x: list(x['longitudeeast']))
    df_latnorth = by_var.apply(lambda x: list(x['latitudenorth']))

    joined_df = df_sitenames.to_frame('sitenames').join(df_siteid.to_frame('siteid')).join(df_longeast.to_frame('longeast')).join(df_latnorth.to_frame('latnorth'))
    joined_df = joined_df.reset_index()
    joined_df = format_coords(joined_df, 'longeast', 'longeast')
    joined_df = format_coords(joined_df, 'latnorth', 'latnorth')
    joined_df = format_sitenames(joined_df, 'sitenames', 'sitenames_l')

    return joined_df
