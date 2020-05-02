import pandas as pd
import numpy as np
import random
from sqlalchemy import create_engine
from api import models
import random


def get_Similar_Store(id):
    id = int(id)
    engine = create_engine(
        'mysql://user:ssafy123!@13.125.100.34:3306/release?charset=utf8mb4')
    conn = engine.connect()
    review_df = pd.read_sql_table('api_review', conn)
    if (review_df[review_df['store_id'] == id].size == 0):
        max = models.Store.objects.count()
        list = [random.randint(0, max) for r in range(10)]
        return list

    s_review = review_df.store_id.unique()
    data = pd.read_pickle('../../data/tf-idf_Result.pkl')
    cur = -1
    group = -1
    for i, e in enumerate(s_review):
        if e == id:
            cur = i
            break
    for i, list1 in enumerate(data):
        if cur in list1:
            group = i
            break

    res = []
    for enum in data[group]:
        res.append(s_review[enum])
    return res


def main():

    id = input("음식점 id 입력:")
    result = get_Similar_Store(id)


if __name__ == "__main__":
    main()
