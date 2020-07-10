import pytest
from src.modules.preprocessing.bibliography_loader import *
import pandas as pd


file = '/Users/seiryu8808/Desktop/UWinsc/Github/Do_not_commit_data/bibjson'
def test_preprocessed_bibliography():
    data = preprocessed_bibliography(file)
    assert isinstance(data, pd.DataFrame)
