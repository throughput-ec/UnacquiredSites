import src.modules.preprocessing.nlp_sentence_loader as sentence_loader
import src.modules.preprocessing.bibliography_loader as bib_loader
import src.modules.preprocessing.add_regex_degrees as ard
import src.modules.preprocessing.neotoma_loader as nl


def get_all_datasets():
    nlp_sentences = sentence_loader.preprocessed_sentences_sql()
    bibliography = bib_loader.preprocessed_bibliography()
    neotoma = nl.neotoma_loader()
    neotoma_joined_df = nl.grouped_coords_df(neotoma)

    return nlp_sentences, bibliography, neotoma, neotoma_joined_df

A = {'_gddid' :  [['ABC'], ['DEF']],
     'States' :  [['Oklahoma'], ['Wisconsin']]}

B = {'_gddid' :  [['ABC'], ['DEF']],
     'doi':  [['Hello'], ['Happy']]}

C = {'doi' :  [['Hello'], ['Happy']],
     'W_Words' :  [['Warning'], ['Wrong']]}

D = {'_gddid'    :  [['ABC'], ['DEF']],
     'States'    :  [['Oklahoma'], ['Wisconsin']],
     'doi'   :  [['Hello'], ['Happy']],
     'W_Words'   :  [['Warning'], ['Wrong']]}

A_df = pd.DataFrame(A, columns = ['_gddid','States'])
B_df = pd.DataFrame(B, columns = ['_gddid', 'doi'])
C_df = pd.DataFrame(C, columns = ['doi', 'W_Words'])
D_df = pd.DataFrame(D, columns = ['_gddid', 'States', 'doi', 'W_Words'])


def test_get_nlp_bib_neotoma():
    new_frames = get_nlp_bib_neotoma(A_df, B_df, C_df)
    assert D.equals(new_frames[1])
