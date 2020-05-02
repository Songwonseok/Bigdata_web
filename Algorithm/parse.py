import json
import pandas as pd
import os
import shutil
from datetime import date
import urllib.request
from bs4 import BeautifulSoup

DATA_DIR = "../data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")
DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")

store_columns = (
    "id",  # 음식점 고유번호
    "store_name",  # 음식점 이름
    "branch",  # 음식점 지점 여부
    "area",  # 음식점 위치
    "tel",  # 음식점 번호
    "address",  # 음식점 주소
    "latitude",  # 음식점 위도
    "longitude",  # 음식점 경도
    "reviewCnt",
    "category",  # 음식점 카테고리
    "image"
)

bhour_columns = (
    "id",
    "type",
    "week_type",
    "mon",
    "tue",
    "wed",
    "thu",
    "fri",
    "sat",
    "sun",
    "start_time",
    "end_time",
    "etc",
    "store"
)
review_columns = (
    "id",  # 리뷰 고유번호
    "store",  # 음식점 고유번호
    "user",  # 유저 고유번호
    "score",  # 평점
    "content",  # 리뷰 내용
    "reg_time",  # 리뷰 등록 시간
)

menu_columns = (
    "id",  # 메뉴 고유번호
    "store",  # 음식점 고유번호
    "menu_name",  # 음식 이름
    "price"  # 음식 가격
)

user_columns = (
    "id",  # 유저 고유 번호
    "gender",  # 유저 성별
    "age"  # 유저 나이
)


def import_data(data_path=DATA_FILE):
    """
    Req. 1-1-1 음식점 데이터 파일을 읽어서 Pandas DataFrame 형태로 저장합니다
    """

    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path}` 가 존재하지 않습니다.")
        exit(1)

    stores = []  # 음식점 테이블
    reviews = []  # 리뷰 테이블
    menus = []  # 메뉴 테이블
    users = []  # 유저 테이블
    bhours = []

    users_set = set([])  # 유저 테이블

    menu_id = 1
    bhour_id = 1
    current_year = date.today().year
    for d in data:

        # parsing하는데 2시간걸려요
        # categories = [c["category"] for c in d["category_list"]]
        # url = 'https://i02a108.p.ssafy.io/assets/' + str(d['id']) + '.jpg'
        # image = ""
        # try:
        #     if d['id'] <= 28312 or 200000 <= d['id'] <= 213225:
        #         res = urllib.request.urlopen(url)
        #         status = res.getcode()
        #         if status == 200:
        #             image = url
        #     else:
        #         image = "https://i02a108.p.ssafy.io/assets/default.jpg"
        # except urllib.error.HTTPError as e:
        #     # print(e.code)
        #     # print(e.reason)
        #     # print(e.headers)
        #     image = "https://i02a108.p.ssafy.io/assets/default.jpg"
        # stores.append(
        #     [
        #         d["id"],
        #         d["name"],
        #         d["branch"],
        #         d["area"],
        #         d["tel"],
        #         d["address"],
        #         d["latitude"],
        #         d["longitude"],
        #         d["review_cnt"],
        #         "|".join(categories),
        #         image
        #     ]
        # )
        for menu in d["menu_list"]:
            menus.append([
                menu_id,
                d["id"],
                menu["menu"],
                menu["price"]
            ])

            menu_id += 1
        for bhour in d["bhour_list"]:
            bhours.append([
                bhour_id,
                bhour["type"],
                bhour["week_type"],
                bhour["mon"],
                bhour["tue"],
                bhour["wed"],
                bhour["thu"],
                bhour["fri"],
                bhour["sat"],
                bhour["sun"],
                bhour["start_time"],
                bhour["end_time"],
                bhour["etc"],
                d["id"]
            ])
            bhour_id += 1
        for review in d["review_list"]:
            r = review["review_info"]
            u = review["writer_info"]

            reviews.append(
                [r["id"], d["id"], u["id"],
                    r["score"], r["content"], r["reg_time"]]
            )
            # if([u["id"], u["gender"], current_year - int(u["born_year"]) ] not in users) :
            #     users.append([u["id"], u["gender"], current_year - int(u["born_year"]) ])

            users_set.add((
                u["id"],
                u["gender"],
                current_year - int(u["born_year"])
            ))

            # 실행시간 if문 28.8  set 5.~ 차이
    users = list(users_set)
    store_frame = pd.DataFrame(data=stores, columns=store_columns)
    review_frame = pd.DataFrame(data=reviews, columns=review_columns)
    menu_frame = pd.DataFrame(data=menus, columns=menu_columns)
    user_frame = pd.DataFrame(data=users, columns=user_columns)
    bhour_frame = pd.DataFrame(data=bhours, columns=bhour_columns)

    return {"stores": store_frame, "reviews": review_frame, "menus": menu_frame, "users": user_frame, "bhours": bhour_frame}


def dump_dataframes(dataframes):
    pd.to_pickle(dataframes, DUMP_FILE)


def load_dataframes():
    return pd.read_pickle(DUMP_FILE)


def main():

    print("[*] Parsing data...")
    data = import_data()
    print("[+] Done")

    print("[*] Dumping data...")
    dump_dataframes(data)
    print("[+] Done\n")

    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    print("[음식점]")
    print(f"{separater}\n")
    print(data["stores"].head())
    print(f"\n{separater}\n\n")

    print("[리뷰]")
    print(f"{separater}\n")
    print(data["reviews"].head())
    print(f"\n{separater}\n\n")

    print("[메뉴]")
    print(f"{separater}\n")
    print(data["menus"].head())
    print(f"\n{separater}\n\n")

    print("[유저]")
    print(f"{separater}\n")
    print(data["users"].head())
    print(f"\n{separater}\n\n")

    print("[영업시간]")
    print(f"{separater}\n")
    print(data["bhours"].head())
    print(f"\n{separater}\n\n")


if __name__ == "__main__":
    main()
