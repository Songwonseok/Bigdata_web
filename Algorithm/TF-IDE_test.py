import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import surprise

def dump_dataframes(dataframes):
    pd.to_pickle(dataframes, DUMP_FILE)

def makestoredump(data):
    df_reviews = data
    df_s_group = df_reviews.groupby(["store"])
    series_over_3 = df_s_group.size()[df_s_group.size() > 10]
    series_over_3_store = series_over_3.to_frame().reset_index()['store']

    over_3_df = pd.DataFrame(columns=["store", "user", "score"])

    user_list = []
    store_list = []
    score_list = []

    for i in series_over_3_store:
        for k in range(df_reviews[df_reviews['store'] == i].id.count()):
            store_list.append(i)
            user_list.append(df_reviews[df_reviews['store'] == i].iloc[k].user)
            score_list.append(df_reviews[df_reviews['store'] == i].iloc[k].score)

    over_3_df["user"] = user_list
    over_3_df["store"] = store_list
    over_3_df["score"] = score_list


    return over_3_df.sort_values(by=['store'])

#딕셔너리로 변형
def recur_dictify(frame):
    if len(frame.columns)==1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k:recur_dictify(g.ix[:,1:]) for k,g in grouped}
    return d

def dic_to_train(data):
    over_3_df = data
    df_to_dict = recur_dictify(over_3_df)

    store_list = []  # 음식점 목록을 담을 리스트
    user_set = set()  # 유저 목록을 담을 set

    # store 수 만큼 반복
    for store_key in df_to_dict:
        store_list.append(store_key)

        for user_key in df_to_dict[store_key]:
            user_set.add(user_key)

    user_list = list(user_set)

    pd.to_pickle(pd.Series(user_list).to_frame(), "../data/Item_based_user_list.pkl")
    pd.to_pickle(pd.Series(store_list).to_frame(), "../data/Item_based_store_list.pkl")

    rating_dic = {
        "store_id": [],
        "user_id": [],
        "score": []
    }

    # store 수 만큼 반복
    for store_key in df_to_dict:
        for name_key in df_to_dict[store_key]:
            a1 = store_list.index(store_key)
            a2 = user_list.index(name_key)
            a3 = df_to_dict[store_key][name_key]

            rating_dic["store_id"].append(a1)
            rating_dic["user_id"].append(a2)
            rating_dic["score"].append(a3)

        df = pd.DataFrame(rating_dic)
    return df.sort_values(by=['store_id'])

def train(dataframe,k):
    # df_to_dict = recur_dictify(pd.read_pickle('../data/over_10review_stores.pkl'))
    store_list = []  # 사용자 목록을 담을 리스트
    # user_set = set()  # 음식점 목록을 담을 set
    #
    # # store 수 만큼 반복
    # for store_key in df_to_dict:
    #     store_list.append(store_key)
    #
    #     for user_key in df_to_dict[store_key]:
    #         user_set.add(user_key)
    #
    # user_list = list(user_set)

    # df = dataframe
    # reader = surprise.Reader(rating_scale=(1, 5))

    # col_list = ['store_id', 'user_id', 'score']
    # data = surprise.Dataset.load_from_df(df[col_list], reader)
    # # Train
    # trainset = data.build_full_trainset()
    # option = {'name': 'pearson'}
    # algo = surprise.KNNBasic(sim_options=option)

    # algo.fit(trainset)

    # 사용자의 음식점을 추천한다.
    # where = input('store id : ')
    # print("\n")

    # user_list = pd.read_pickle("../data/Item_based_user_list.pkl")[0].tolist()
    # store_list = pd.read_pickle("../data/Item_based_store_list.pkl")[0].tolist()
    # user_list = dff.user.unique().tolist()
    # store_list = dff.store.unique().tolist()

    # index = store_list.index(int(where))
    # print('store_idx : ', index)
    # print("\n")

    # result = algo.get_neighbors(index, k=k)  # k=10
    # print(where, "와 유사한 음식점은?")
    # print(result)
    # print("\n")

    # # 음식점에 대한 유저를 추천한다.
    # print(where, "를 평가한 당신에게 추천하는 친구:", "\n")

    # for r1 in result:
    #     max_rating = data.df[data.df["store_id"] == r1]["score"].max()
    #     user_id = data.df[(data.df["score"] == max_rating) & (data.df["store_id"] == r1)]["user_id"].values

    #     for user in user_id:
    #         print(user_list[user])

def main():
    # print("make dump file")
    data = pd.read_pickle("../data/dump.pkl")
    data = data['reviews']
    contents_review = pd.DataFrame(columns=["id", "content"])
    id_list = []
    content_list = []

    print(data['content'])

    for i in data:
        id_list.append(i)    
    content_list.append(data['content'])
        # content_list.append(data['content'].iloc[i])

    print(content_list)

    contents_review["id"] = id_list
    contents_review["content"] = content_list
    print(contents_review)
    # over_3_df = makestoredump(data['reviews'])
    # pd.to_pickle(over_3_df,"../data/over_10review_stores.pkl")
    # print("end of make dump file")
    #
    # print("dic to train")
    # data = pd.read_pickle("../data/over_10review_stores.pkl")
    # frame = dic_to_train(data)
    # pd.to_pickle(frame,"../data/dic_to_train_stores.pkl")
    # print("end of dic to train")

    # data = pd.read_pickle("../data/dic_to_train_stores.pkl")
    # train(data,10)

if __name__ == "__main__":
    main()