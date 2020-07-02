# Functions to add regex degrees

dms_regex = r"([-]?\d{1,3}[°|′|\'|,]{0,3}\d{1,2}[,|′|\']{1,3}\d{0,2}[,|′|\']{1,4}[NESWnesw]?[\s|,|\']+?[-]?\d{1,3}[°|,|′|\']+\d{1,2}[,|′|\']+\d{0,2}[,|′|\'][,|′|\']{0,4}[NESWnesw]?)"
dd_regex =  r"([-]?\d{1,3}\.\d{1,}[,]?[NESWnesw][\s|,|\']+?[-]?\d{1,3}\.\d{1,}[,]?[NESWnesw])"


def convert_words_to_string(df, col_to_convert = 'col', new_col_name = 'words_as_string'):
    df[new_col_name] = df[col_to_convert].apply(lambda x: ','.join(map(str, x)))
    return df

# Add columns to dataframe for the dms and dd REGEX
def add_dms_re(df, search_col = 'col', new_col_name = 'dms_regex'):
    '''Add coordinates degree minutes second format
    Example:
    nlp_sentences = add_regex_degrees.add_dms_re(nlp_sentences, 'words_as_string', 'dms_regex')
    '''
    df[new_col_name] = df[search_col].str.findall(dms_regex)
    return df

def add_dd_re(df, search_col = 'col', new_col_name = 'dd_regex'):
    '''Add coordinates degree minutes second format
    Example:
    nlp_sentences = add_dd_re(nlp_sentences, 'words_as_string', 'dd_regex')
    '''
    df[new_col_name] = df[search_col].str.findall(dd_regex)
    return df

def find_digits_from_words(df, search_col = 'col', new_col_name = 'digits_from_words'):
    df[new_col_name] = df[search_col].str.findall(r'\d+')
    return df

def order_article(df, article_id, order_by = 'sentid', show_cols = 'words'):
    '''
    Function to find an article by its gddid in the NLP sentences and have it displayed in order

    Keyword arguments:
    article_id -- gddid

    Returns:
    article ordered by sentence index
    '''
    article = df[df['_gddid'] == article_id]
    return article[[order_by, show_cols]].sort_values(by = order_by)
