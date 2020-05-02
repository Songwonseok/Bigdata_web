import numpy as np
import pandas as pd
import konlpy
from konlpy.tag import Hannanum
from konlpy.tag import Twitter
import random
import math
import copy
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
import pickle
from sklearn.cluster import KMeans
from sqlalchemy import create_engine


def main():
    engine = create_engine(
        'mysql://user:ssafy123!@13.125.100.34:3306/release?charset=utf8mb4')
    conn = engine.connect()
    review_df = pd.read_sql_table('api_review', conn)
    s_review = review_df.store_id.unique()
    tot_rev_df = pd.DataFrame(columns=["store", "contents"])

    revlist = []
    for i in s_review:
        str = ""
        for content in review_df[review_df.store_id == i].content:
            str = str + " " + content
        revlist.append(str)

    tot_rev_df["store"] = s_review
    tot_rev_df["contents"] = revlist

    twitter = Twitter()

    all = []

    for i in range(0, len(tot_rev_df)):
        if (len(tot_rev_df.loc[i].contents) == 1):
            temp = []
        else:
            temp = twitter.nouns(tot_rev_df.loc[i].contents)
        all.append(temp)
    tfMapList = []
    wordMap = {}
    wordCount = 0

    for data in all:
        tfMap = {}
        for word in data:
            if word in tfMap.keys():
                tfMap[word] += 1
            else:
                tfMap[word] = 1

            if word not in wordMap.keys():
                wordMap[word] = wordCount
                wordCount += 1

        tfMapList.append(tfMap)

    table = [[0] * len(wordMap) for _ in range(len(tfMapList))]
    row = 0
    for tfMap in tfMapList:
        for word, tf in tfMap.items():
            word_count = 0
            for map1 in tfMapList:
                if word in map1.keys():
                    word_count += 1

            idf = math.log10(len(tfMapList) / word_count)
            tf_idf = tf * idf
            column = wordMap[word]
            table[row][column] = tf_idf

    table2 = pd.DataFrame.from_records(table)

    svd = TruncatedSVD(n_components=15)
    pos = svd.fit_transform(table2)

    norm = Normalizer(copy=False)
    pos2 = norm.fit_transform(pos)

    km = KMeans(n_clusters=40, random_state=0)
    labels_km = km.fit_predict(pos2)

    result = []
    for cur in range(0, 40):
        temp = [i for i, e in enumerate(labels_km) if e == cur]
        result.append(temp)

    with open('../../../../data/tf-idf_Result.pkl', 'wb') as f:
        pickle.dump(result, f)


if __name__ == "__main__":
    main()
