import src.modules.preprocessing.preprocess_all_data as data_creator
import src.modules.preprocessing.add_regex_degrees as ard
import os

def load_all_data():
    nlp_sentences, bibliography, neotoma, neotoma_joined_df = data_creator.get_all_datasets()
    nlp_bib, nlp_bib_neotoma = data_creator.get_nlp_bib_neotoma(nlp_sentences, bibliography, neotoma_joined_df)
    return nlp_sentences, bibliography, neotoma, neotoma_joined_df, nlp_bib, nlp_bib_neotoma

def not_in_neotoma(df, df2, path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output'):
    arts_not_in_neotoma = df[df['longeast'].isnull()]
    arts_not_in_neotoma = arts_not_in_neotoma.groupby('_gddid')\
                                             .agg({'longeast':'sum'})

    arts_not_in_neotoma = arts_not_in_neotoma.merge(df2, on ='_gddid')
    arts_not_in_neotoma = arts_not_in_neotoma[['_gddid', 'title', 'year', 'doi', 'link_url']]
    
    output_file = os.path.join(path,'articles_wo_neotoma_coordinates.tsv')
    arts_not_in_neotoma.to_csv(output_file, sep='\t', index = False)
    print("A TSV file was created on your output folder.")
    return arts_not_in_neotoma

def sentences_w_coords_int(df_with_int, path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output'):
    # Output of sentences with lat and long intersections
    sent_with_int_df = df_with_int[['_gddid','words', 'year', 'latnorth', 'intersection_words_lat', 'longeast', 'intersection_words_long', 'dms_regex',  'dd_regex']]
    sent_with_int_df = sent_with_int_df.rename(columns={"latnorth":"expected_lat", 'intersection_words_lat':'intersection_lat', 'longeast':'expected_long', 'intersection_words_long':'intersection_long'})
    output_file = os.path.join(path,'sentences_with_latlong_intersections.tsv')
    sent_with_int_df.to_csv(output_file, sep='\t', index = False)
    print("A TSV file was created on your output folder.")
    return sent_with_int_df

def articles_wo_coords(nlp_bib_neotoma, bibliography, neotoma_joined_df, path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output'):
    # No article - coordinates intersections DF
    no_inter_df = nlp_bib_neotoma.groupby('_gddid')\
                    .agg({'intersection_words_lat':'sum', 'intersection_words_long':'sum'})\
                    .reset_index()

    no_inter_df = no_inter_df[(no_inter_df['intersection_words_lat'].apply(len) == 0) & (no_inter_df['intersection_words_long'].apply(len) == 0 )]

    
    no_inter_df = no_inter_df.merge(bibliography)
    no_inter_df = no_inter_df.merge(neotoma_joined_df, how = 'left', left_on = 'doi', right_on = 'doi')\
                             .rename(columns={"latnorth": "expected_lat", "longeast": "expected_long"})
    no_inter_df = no_inter_df[['_gddid', 'title', 'year','intersection_words_lat', 'expected_lat', 'intersection_words_long', 'expected_long', 'doi', 'link_url',]]
    output_file = os.path.join(path,'articles_wo_latlong_intersections.tsv')
    no_inter_df.to_csv(output_file, sep='\t', index = False)
    print("A TSV file was created on your output folder.")
    return no_inter_df



def sentences_w_site_int(nlp_bib_neotoma, path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output'):
    sn_inter = ard.find_intersections(nlp_bib_neotoma, cols_to_intersect = ['words_l','sitenames_l'], new_col_name = 'intersection_words_sitenames')

    sn_inter = sn_inter[sn_inter['intersection_words_sitenames'].str.len() != 0]

    sn_inter = sn_inter[['_gddid', 'sentid', 'words_l', 'sitenames_l', 'intersection_words_sitenames', 'year']]
    sn_inter = sn_inter.rename(columns={'sitenames_l':'expected_sitename','intersection_words_sitenames':'intersected_sitename'})
    output_file = os.path.join(path,'sentences_with_sitenames_intersections.tsv')
    sn_inter.to_csv(output_file, sep='\t', index = False)
    print("A TSV file was created on your output folder.")
    return sn_inter

def articles_wo_sites(nlp_bib_neotoma, bibliography, neotoma_joined_df, path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output'):
    arts_wo_sites = nlp_bib_neotoma.groupby('_gddid')\
                                                       .agg({'intersection_words_sitenames':'sum'})\
                                                       .reset_index()

    arts_wo_sites['intersection_words_sitenames'] = arts_wo_sites['intersection_words_sitenames'].apply(lambda x: list(set(x)))
    arts_wo_sites = arts_wo_sites[arts_wo_sites['intersection_words_sitenames'].str.len() == 0]
    arts_wo_sites = arts_wo_sites.merge(bibliography, how = 'inner')\
                                 .merge(neotoma_joined_df, left_on = 'doi', right_on = 'doi')
    
    arts_wo_sites = arts_wo_sites[['_gddid', 'title', 'year','intersection_words_sitenames', 'sitenames', 'doi', 'link_url']]
    arts_wo_sites = arts_wo_sites.rename(columns = {'sitenames': 'exptected_sitename'})
    
    # Output file
    output_file = os.path.join(path,'articles_wo_sitename_intersections.tsv')
    arts_wo_sites.to_csv(output_file, sep='\t', index = False)
    print("A TSV file was created on your output folder.")
    
    return arts_wo_sites
