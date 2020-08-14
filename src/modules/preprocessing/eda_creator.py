import utils as ard
import os

def not_in_neotoma(df, df2, path = r'src/output/eda'):
    """Obtain all the article DOI's that are not in the Neotoma Database

    Parameters
    ----------
    df : pd.DataFrame
        Input data frame
    df2: pd.DataFrame
         Input data frame
    path: location where to write csv file

    Returns
    -------
    pd.DataFrame with values that are not contained in the Neotoma Database
    csv file in the output path with the mentioned DataFrame

    """
    arts_not_in_neotoma = df[df['longeast'].isnull()]
    arts_not_in_neotoma = arts_not_in_neotoma.groupby('_gddid')\
                                             .agg({'longeast':'sum'})

    arts_not_in_neotoma = arts_not_in_neotoma.merge(df2, on ='_gddid')
    arts_not_in_neotoma = arts_not_in_neotoma[['_gddid', 'title', 'year', 'doi', 'link_url']]

    output_file = os.path.join(path,'articles_wo_neotoma_coordinates.tsv')
    arts_not_in_neotoma.to_csv(output_file, sep='\t', index = False)
    print("A TSV file with articles not found in Neotoma was created on your EDA output folder.")
    return arts_not_in_neotoma

def sentences_w_coords_int(df_with_int, path = r'src/output/eda'):
    """Obtain all the intersections between sentences in NLP df and Neotoma DB

    Parameters
    ----------
    df_with_int : pd.DataFrame
        Input data frame where we want to look for intersections

    path: location where to write csv file

    Returns
    -------
    pd.DataFrame with coordinate intersections between sentences and neotoma database
    csv file in the output path with the mentioned DataFrame

    """
    # Output of sentences with lat and long intersections
    sent_with_int_df = df_with_int[['_gddid','words', 'year', 'latnorth', 'found_lat', 'longeast', 'found_long', 'dms_regex',  'dd_regex']]
    sent_with_int_df = sent_with_int_df.rename(columns={"latnorth":"expected_lat", 'longeast':'expected_long'})
    output_file = os.path.join(path,'sentences_with_latlong_intersections.tsv')
    sent_with_int_df.to_csv(output_file, sep='\t', index = False)
    print("A TSV file with sentences that have coordinates was created in your EDA output folder.")
    return sent_with_int_df

def articles_wo_coords(nlp_bib_neotoma, bibliography, neotoma_joined_df, path = r'src/output/eda'):
    """Obtain all article that have no coordinate intersections

    Parameters
    ----------
    df = nlp_bib_neotoma : pd.DataFrame
        Input data frame
    df2 = bibliography : pd.DataFrame
        Input data frame
    df3 = neotoma_joined_df :pd.DataFrame
        Input data frame

    path: location where to write csv file

    Returns
    -------
    pd.DataFrame with articles that have no coordinates in the Neotoma Database
    csv file in the output path with the mentioned DataFrame

    """
    no_inter_df = nlp_bib_neotoma.groupby('_gddid')\
                    .agg({'found_lat':'sum', 'found_long':'sum'})\
                    .reset_index()

    no_inter_df = no_inter_df[(no_inter_df['found_lat'].apply(len) == 0) & (no_inter_df['found_long'].apply(len) == 0 )]


    no_inter_df = no_inter_df.merge(bibliography)
    no_inter_df = no_inter_df.merge(neotoma_joined_df, how = 'left', left_on = 'doi', right_on = 'doi')\
                             .rename(columns={"latnorth": "expected_lat", "longeast": "expected_long"})
    no_inter_df = no_inter_df[['_gddid', 'title', 'year','found_lat', 'expected_lat', 'found_long', 'expected_long', 'doi', 'link_url',]]
    output_file = os.path.join(path,'articles_wo_latlong_intersections.tsv')
    no_inter_df.to_csv(output_file, sep='\t', index = False)
    print("A TSV file of articles that have no coordinates was created in your EDA output folder.")
    return no_inter_df



def sentences_w_site_int(nlp_bib_neotoma, path = r'src/output/eda'):
    """Obtain all article that have no coordinate intersections

    Parameters
    ----------
    df = nlp_bib_neotoma : pd.DataFrame
        Input data frame

    path: location where to write csv file

    Returns
    -------
    pd.DataFrame with intersections of sitenames and sentences df
    csv file in the output path with the mentioned DataFrame

    """
    sn_inter = ard.find_intersections(nlp_bib_neotoma, cols_to_intersect = ['words_l','sitenames_l'], new_col_name = 'found_sitenames')

    sn_inter = sn_inter[sn_inter['found_sitenames'].str.len() != 0]

    sn_inter = sn_inter[['_gddid', 'sentid', 'words_l', 'sitenames_l', 'found_sitenames', 'year']]
    sn_inter = sn_inter.rename(columns={'sitenames_l':'expected_sitename','found_sitenames':'intersected_sitename'})
    output_file = os.path.join(path,'sentences_with_sitenames_intersections.tsv')
    sn_inter.to_csv(output_file, sep='\t', index = False)
    print("A TSV file of sentences with Site intersections was created in your EDA output folder.")
    return sn_inter

def articles_wo_sites(nlp_bib_neotoma, bibliography, neotoma_joined_df, path = r'src/output/eda'):
    """Obtain all article that have no sitenames intersections

    Parameters
    ----------
    df = nlp_bib_neotoma : pd.DataFrame
        Input data frame
    df2 = bibliography : pd.DataFrame
        Input data frame
    df3 = neotoma_joined_df :pd.DataFrame
        Input data frame

    path: location where to write csv file

    Returns
    -------
    pd.DataFrame with articles that have no sitenames in the Neotoma Database
    csv file in the output path with the mentioned DataFrame

    """
    arts_wo_sites = nlp_bib_neotoma.groupby('_gddid')\
                                                       .agg({'found_sitenames':'sum'})\
                                                       .reset_index()

    arts_wo_sites['found_sitenames'] = arts_wo_sites['found_sitenames'].apply(lambda x: list(set(x)))
    arts_wo_sites = arts_wo_sites[arts_wo_sites['found_sitenames'].str.len() == 0]
    arts_wo_sites = arts_wo_sites.merge(bibliography, how = 'inner')\
                                 .merge(neotoma_joined_df, left_on = 'doi', right_on = 'doi')

    arts_wo_sites = arts_wo_sites[['_gddid', 'title', 'year','found_sitenames', 'sitenames', 'doi', 'link_url']]
    arts_wo_sites = arts_wo_sites.rename(columns = {'sitenames': 'exptected_sitename'})

    # Output file
    output_file = os.path.join(path,'articles_wo_sitename_intersections.tsv')
    arts_wo_sites.to_csv(output_file, sep='\t', index = False)
    print("A TSV file of Articles without Sites was created in your EDA output folder.")

    return arts_wo_sites
