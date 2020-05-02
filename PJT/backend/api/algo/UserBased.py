import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import surprise
from sqlalchemy import create_engine

DATA_DIR = "../../../../data"
DUMP_FILE = os.path.join(DATA_DIR, "over_3review_peoples.pkl")


def dump_dataframes(dataframes):
    pd.to_pickle(dataframes, DUMP_FILE)


def makeuserdump(data):
    df_reviews = data
    df_r_group = df_reviews.groupby(["user_id"])
    series_over_3 = df_r_group.size()[df_r_group.size() > 10]
    series_over_3_user = series_over_3.to_frame().reset_index()['user_id']

    over_3_df = pd.DataFrame(columns=["user", "store", "score"])

    user_list = []
    store_list = []
    score_list = []

    for i in series_over_3_user:
        for k in range(df_reviews[df_reviews['user_id'] == i].id.count()):
            user_list.append(i)
            store_list.append(
                df_reviews[df_reviews['user_id'] == i].iloc[k].store_id)
            score_list.append(
                df_reviews[df_reviews['user_id'] == i].iloc[k].score)

    over_3_df["user"] = user_list
    over_3_df["store"] = store_list
    over_3_df["score"] = score_list

    return over_3_df.sort_values(by=['user'])


def dic_to_train(data):
    over_3_df = data
    df_to_dict = recur_dictify(over_3_df)

    name_list = []  # user list
    store_set = set()  # store set

    # Iterate as # of users
    for user_key in df_to_dict:
        name_list.append(user_key)

        for sto_key in df_to_dict[user_key]:
            store_set.add(sto_key)

    store_list = list(store_set)
    pd.to_pickle(pd.Series(name_list).to_frame(),
                 "../../../../data/user_based_name_list.pkl")
    pd.to_pickle(pd.Series(store_list).to_frame(),
                 "../../../../data/user_based_store_list.pkl")

    rating_dic = {
        "user_id": [],
        "store_id": [],
        "score": []
    }
    # Iterate as # of users
    for name_key in df_to_dict:
        for sto_key in df_to_dict[name_key]:
            a1 = name_list.index(name_key)
            a2 = store_list.index(sto_key)
            a3 = df_to_dict[name_key][sto_key]

            rating_dic["user_id"].append(a1)
            rating_dic["store_id"].append(a2)
            rating_dic["score"].append(a3)

    df = pd.DataFrame(rating_dic)
    return df.sort_values(by=['user_id'])


# Change to dictionary
def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1:
            return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.ix[:, 1:]) for k, g in grouped}
    return d


def train(who, k):
    # df_to_dict = recur_dictify(pd.read_pickle('../../../data/over_10review_peoples.pkl'))
    # name_list = []  # User list
    # store_set = set()  # Store set
    #
    # # Iterate as # of users
    # for user_key in df_to_dict:
    #     name_list.append(user_key)
    #
    #     for sto_key in df_to_dict[user_key]:
    #         store_set.add(sto_key)
    #
    # store_list = list(store_set)

    df = pd.read_pickle("../../data/dic_to_train.pkl")
    reader = surprise.Reader(rating_scale=(1, 5))
    col_list = ['user_id', 'store_id', 'score']
    data = surprise.Dataset.load_from_df(df[col_list], reader)
    # Train
    trainset = data.build_full_trainset()
    option = {'name': 'pearson'}
    algo = surprise.KNNBasic(sim_options=option)

    algo.fit(trainset)

    name_list = pd.read_pickle(
        "../../data/user_based_name_list.pkl")[0].tolist()
    store_list = pd.read_pickle(
        "../../data/user_based_store_list.pkl")[0].tolist()
    # name_list = dff.user.unique().tolist()
    # store_list = dff.store.unique().tolist()

    index = name_list.index(int(who))

    result = algo.get_neighbors(index, k=k)  # k=5

    # Recommend store to user
    recommend_store_list = []

    for r1 in result:
        max_rating = data.df[data.df["user_id"] == r1]["score"].max()
        sto_id = data.df[(data.df["score"] == max_rating) & (
            data.df["user_id"] == r1)]["store_id"].values

        for sto in sto_id:
            recommend_store_list.append(store_list[sto])
    return recommend_store_list


def main():

    engine = create_engine(
        'mysql://user:ssafy123!@13.125.100.34:3306/release?charset=utf8mb4')
    conn = engine.connect()
    reviews = pd.read_sql_table('api_review', conn)
    over_3_df = makeuserdump(reviews)
    pd.to_pickle(over_3_df, "../../../../data/over_10review_peoples.pkl")

    data = pd.read_pickle("../../../../data/over_10review_peoples.pkl")
    frame = dic_to_train(data)
    pd.to_pickle(frame, "../../../../data/dic_to_train.pkl")

    # recommend_store = train(950340, 5)


if __name__ == "__main__":
    main()
