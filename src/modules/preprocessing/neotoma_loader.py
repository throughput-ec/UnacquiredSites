import pandas as pd
import os
import ast
from nltk.tokenize import word_tokenize


def neotoma_loader(file = "/Users/seiryu8808/Desktop/UnacquiredSites2/data/Do_not_commit_data/data-1590729612420.csv"):
    neotoma = pd.read_csv(file)
    neotoma = neotoma[['siteid', 'sitename', 'longitudeeast', 'latitudenorth', 'longitudewest', 'latitudesouth', 'sitedescription', 'doi']]
    return neotoma

def format_coords(df, col_to_convert, col_new_name):
    df[col_new_name] = df[col_to_convert].apply(lambda x: [int(abs(i)) for i in x])\
                                         .apply(lambda x: [str(i) for i in x])\
                                         .replace('-', '', regex = True)\
                                         .apply(lambda x: list(set(x)))
    return df

def format_sitenames(df, col_to_convert, col_new_name):
    df[col_new_name] = df[col_to_convert].astype(str).str.lower().transform(ast.literal_eval)\
                                         .apply(lambda x: [word_tokenize(i) for i in x])\
                                         .apply(lambda l: [item for sublist in l for item in sublist])\
                                         .apply(lambda x: list(set(x)))
    return df


def grouped_coords_df(df, group_by_var = 'doi'):
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
