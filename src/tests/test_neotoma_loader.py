import pytest
from src.modules.preprocessing.neotoma_loader import *
import pandas as pd

file = "/Users/seiryu8808/Desktop/UWinsc/Github/Do_not_commit_data/data-1590729612420.csv"

def test_neotoma_loader():
    data = neotoma_loader(file)
    assert isinstance(data, pd.DataFrame)

# Creating some test DataFrame
test_data = {'First_Col' :  [[-13], [10.5]],
             'Second_Col':  [['Oklahoma'], ['Wisconsin']]}

expected_res = {'Tested_First_Col' :  [[13], [10]],
                'Tested_Second_Col':  [['oklahoma'], ['wisconsin']]}


test_df = pd.DataFrame(test_data, columns = ['First_Col','Second_Col'])
expected_res = pd.DataFrame(expected_res, columns = ['Tested_First_Col', 'Tested_Second_Col'])

def test_format_coords(test_df = test_df, expected_res = expected_res):
    test_df = format_coords(test_df, 'First_Col', 'New_Col')
    assert test_df['New_Col'].iloc[0] == ['13']
    assert test_df['New_Col'].iloc[1] == ['10']


def test_dtype_format_coords(test_df = test_df):
    test_df = format_coords(test_df, 'First_Col', 'New_Col')
    assert isinstance(test_df['New_Col'].iloc[0], list)


def test_format_sitenames(test_df = test_df, expected_res = expected_res):
    test_df = format_sitenames(test_df, 'Second_Col', 'New_Col')
    assert test_df['New_Col'].equals(expected_res['Tested_Second_Col'])
