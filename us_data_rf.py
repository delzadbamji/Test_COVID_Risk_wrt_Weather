import os
import sqlite3

import pandas as pd
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle


def runClassifier(df, label):
    features = df.to_numpy()

    size = features.shape[0]

    indexArr = np.random.choice(range(size), int(size * 0.7), replace=False)
    print(features.shape)
    features = features[indexArr]
    label = label[indexArr]

    clf = RandomForestClassifier(n_estimators=50, max_depth=16,
                                 n_jobs=-1, max_samples=0.8)
    where_are_NaNs = np.isnan(features)
    features[where_are_NaNs] = 0
    clf.fit(features, label)
    print(clf.score(features, label))
    filename = 'us_data_clf'
    pickleFile = open(filename, 'wb')
    pickle.dump(clf, pickleFile)
    pickleFile.close()


def fun(conn, fileToClf, first):
    query = "select * from us_data where date in (select  distinct date from us_data order by date asc limit 1);"
    df = pd.read_sql_query(query, conn)

    file = open(fileToClf, 'rb')
    clf = pickle.load(file)
    deleteAttributes(df, ["risk", "id", "date", "fatality_ratio"])
    one_hot = pd.get_dummies(df.Province, prefix='Province')
    second = set(one_hot.columns)
    print(first - second)
    # Drop column B as it is now encoded
    df = df.drop('Province', axis=1)
    df = df.join(one_hot)

    # print(len(df.columns))
    features = df.to_numpy()
    print(features.shape)
    where_are_NaNs = np.isnan(features)
    features[where_are_NaNs] = 0
    probArr = clf.predict_proba(features)
    print(probArr)
    prediction = clf.predict(features)
    print(features[:, 1], features[:, 2])
    return features[:, 1], features[:, 2], prediction, probArr


def deleteAttributes(df, names):
    for name in names:
        del df[name]


def main():
    conn = sqlite3.connect('coviddb.db')
    query = "select * from us_data where Province <> 'Recovered';"
    df = pd.read_sql_query(query, conn)
    columns = df.columns.values
    print(columns)
    mean = df["fatality_ratio"].mean()

    df = df.fillna(value={"fatality_ratio": mean})
    print(df.head())
    label = df["risk"].to_numpy()
    df.loc[df.fatality_ratio > mean, "risk"] = 1
    df.loc[df.fatality_ratio < mean, "risk"] = 0
    deleteAttributes(df, ["risk", "id", "date", "fatality_ratio"])

    one_hot = pd.get_dummies(df.Province, prefix='Province')
    first = set(one_hot.columns)
    df = df.drop('Province', axis=1)
    df = df.join(one_hot)
    runClassifier(df, label)
    fun(conn, "us_data_clf", first)


if __name__ == '__main__':
    main()
