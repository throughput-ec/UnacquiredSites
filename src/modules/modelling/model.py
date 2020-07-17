def prepare_data(data = data):
    data['has_both_lat_long_int'] = ((data['intersection_words_lat'].apply(len) != 0) & (data['intersection_words_long'].apply(len) != 0 ))

    # Map True to One and False to Zero
    data['has_both_lat_long_int'] = data['has_both_lat_long_int'].astype(int)

    # Reduce data to columns of interest for this task.
    data = data[['words_as_string', 'has_both_lat_long_int']]

    # Define corpus for CountVectorizer
    corpus = data['words_as_string'].tolist()

    # Split data into training and testing sets
    data_train, data_test = train_test_split(data, test_size = 0.20, random_state = 12)

    # Translate words to vectors
    # NLP model
    vec = CountVectorizer(min_df=2,
                          tokenizer=nltk.word_tokenize)

    # Fit and transform training
    X_train = vec.fit_transform(data_train['words_as_string'])
    y_train = data_train['has_both_lat_long_int']

    # Transform test data without fitting
    X_test = vec.transform(data_test['words_as_string'])
    y_test = data_test['has_both_lat_long_int']

    return X_train, y_train, X_test, y_test, data

X_train, y_train, X_test, y_test, data = prepare_data(data = data)

clf = DecisionTreeClassifier(min_samples_split = 40, max_depth = 12)
clf.fit(X_train, y_train)
