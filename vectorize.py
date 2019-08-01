import pandas
import os
import numpy as np


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

if __name__ == '__main__':

    pandas.set_option('display.max_rows', 500)
    pandas.set_option('display.max_columns', 500)
    pandas.set_option('display.width', 10000)

    df1 = pandas.read_csv(os.path.join('data', 'dataset1.tsv'), sep='\t', parse_dates=['date'])
    df1.sort_values(by=['date'], inplace=True)
    df1['returns'] = np.log(df1['Close'] / df1['Close'].shift(1))
    df1['returns'].fillna(0)
    df1['returns_1'] = df1['returns'].fillna(0)
    df1['returns_2'] = df1['returns_1'].replace([np.inf, -np.inf], np.nan)
    df1['returns_final'] = df1['returns_2'].fillna(0)

    df2 = pandas.read_csv(os.path.join('data', 'dataset2.tsv'), sep='\t', parse_dates=['date'])
    df2.sort_values(by=['date'], inplace=True)
    df2['returns'] = np.log(df2['Close'] / df2['Close'].shift(1))
    df2['returns'].fillna(0)
    df2['returns_1'] = df2['returns'].fillna(0)
    df2['returns_2'] = df2['returns_1'].replace([np.inf, -np.inf], np.nan)
    df2['returns_final'] = df2['returns_2'].fillna(0)

    df3 = pandas.read_csv(os.path.join('data', 'dataset3.tsv'), sep='\t', parse_dates=['date'])
    df3.sort_values(by=['date'], inplace=True)
    df3['returns'] = np.log(df3['Close'] / df3['Close'].shift(1))
    df3['returns'].fillna(0)
    df3['returns_1'] = df3['returns'].fillna(0)
    df3['returns_2'] = df3['returns_1'].replace([np.inf, -np.inf], np.nan)
    df3['returns_final'] = df3['returns_2'].fillna(0)

    frames = [df1, df2, df3]
    df4 = pandas.concat(frames, ignore_index=True)



    texts = df4['news']
    tfidf = TfidfVectorizer()
    x = tfidf.fit_transform(texts)
    y = df4['returns_final']
    y = [1 if yi >= 0 else -1 for yi in y]

    X_train, X_test, y_train, y_test = train_test_split(x, y, shuffle=False)

    print(X_train.shape[0])
    print(X_test.shape[0])

    clf = LogisticRegression(solver='lbfgs', n_jobs=-1)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))