# Add columns to dataframe for the dms and dd REGEX

def find_regex(df,
            find_val='dms_regex',
            search_col='col',
            new_col_name='dms_regex'):
    """
    Finds all REGEX expressions within a column

    Parameters
    ----------
    df : pd.DataFrame
        Input data frame
    find_val : string
        Kind of REGEX to look for
    search_col : df column
        Column that contains string with REGEX of interest.
    new_col_name : df column
        Name of the new column that will contain the found REGEX

    Returns
    -------
    pd.DataFrame with new column
    This new column contains the list REGEX of interest
    """

    rxDict = {'dms_regex': r"([-]?\d{1,3}[°|′|\'|,]{0,3}\d{1,2}[,|′|\']{1,3}\d{0,2}[,|′|\']{1,4}[NESWnesw]?[\s|,|\']+?[-]?\d{1,3}[°|,|′|\']+\d{1,2}[,|′|\']+\d{0,2}[,|′|\'][,|′|\']{0,4}[NESWnesw]?)",
              'dd_regex':  r"([-]?\d{1,3}\.\d{1,}[,]?[NESWnesw][\s|,|\']+?[-]?\d{1,3}\.\d{1,}[,]?[NESWnesw])",
              'digits_regex': r"\d+"}

    df[new_col_name] = df[search_col].str.findall(rxDict[find_val])

    return df


def order_article(df, article_id, order_by='sentid', show_cols='words'):
    """
    Orders NLP database articles by sentence ID

    Parameters
    ----------
    df : pd.DataFrame
        Input data frame, NLP sentences for our study
    order_by : string
        Chosen column to order database by
    show_cols : df column
        Visualized column of corpi.

    Returns
    -------
    pd.DataFrame ordered by chosen column.
    """
    article = df[df['_gddid'] == article_id]
    return article[[order_by, show_cols]].sort_values(by=order_by)


def find_intersections(df, cols_to_intersect=[], new_col_name='new_col'):
    """
    Finds all intersections between two columns and performs a set operation
    in order to return the values just once.

    Parameters
    ----------
    df : pd.DataFrame
        Input data frame
    cols_to_intersect : string
        Columns which intersection we are looking for.
    new_col_name : string
        New Column that contains cols_to_intersect intersection.

    Returns
    -------
    pd.DataFrame with new column
    This new column contains the intersections between the given columns in
    the second argument
    """
    df[new_col_name] = df[cols_to_intersect]\
        .apply(lambda x: list(set.intersection(*map(set, list(x)))), axis=1)

    return df
