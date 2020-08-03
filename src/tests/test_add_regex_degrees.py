import pytest
from src.modules.preprocessing.add_regex_degrees import *
import pandas as pd

# Testing Data
test_data = {'Words'      : [['this', 'is', 'a', 'sentence'], ['hello']],
             'Regex_Col'  : ['this,is,a,sentence,with,403,56,40,N,,,153,36,48,E', 'hello'],
             'Int_Checker': [['hello','sentence'], ['whatever']],
             }

expected_res = {'Tested_Words_To_String' :  ['this,is,a,sentence', 'hello'],
                'Tested_Second_Col'      :  [['403,56,40,N,,,153,36,48,E'], []],
                'Int_Results'            :  [['sentence'], []]}

test_df = pd.DataFrame(test_data, columns = ['Words','Regex_Col','Int_Checker'])
expected_res = pd.DataFrame(expected_res, columns = ['Tested_Words_To_String', 'Tested_Second_Col','Int_Results'])


def test_convert_words_to_string(df = test_df):
    convert_words_to_string(test_df, 'Words', 'Tested_Words')
    assert test_df['Tested_Words'].equals(expected_res['Tested_Words_To_String'])


# Test Regex finder
def test_find_re(df = test_df):
    '''Add coordinates degree minutes second format
    Example:
    nlp_sentences = add_regex_degrees.add_dms_re(nlp_sentences, 'words_as_string', 'dms_regex')
    '''
    test_df = find_re(df, find_val = 'dms_regex', search_col = 'Regex_Col', new_col_name = 'REGEX')
    assert test_df['REGEX'].equals(expected_res['Tested_Second_Col'])


def test_find_intersections(df = test_df, cols_to_intersect = [], new_col_name = 'new_col'):
    test_df = find_intersections(df, ['Words', 'Int_Checker'], 'Int_Tester')
    assert test_df['Int_Tester'].equals(expected_res['Int_Results'])
