import json
import pandas as pd
import os
import shutil
from datetime import date
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup

DATA_DIR = "../data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")
DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")


def crawling(data_path=DATA_FILE):

    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path}` 가 존재하지 않습니다.")
        exit(1)

    for d in data:
        if d['id'] < 7110:
            continue
        if d['area'] is not None:
            tmp = (d['name'] + " " + d['area']).replace(" ", "+")
        else:
            tmp = d['name'].replace(" ", "+")
        url = 'https://www.diningcode.com/isearch.php?query=' + quote(tmp)
        try:
            res = urllib.request.urlopen(url)
            status = res.getcode()
            if status == 200:
                res = res.read()
                soup = BeautifulSoup(res, 'html.parser')
                soup = soup.find('div', {'id': 'div_rn'})
                if soup is not None:  # 검색결과 있을 때만
                    imgUrl = soup.find('div', class_='img')[
                        "style"].split(" ")[1]
                    imgUrl = imgUrl.split("\'")[1]
                    status = urllib.request.urlopen(imgUrl).getcode()

                    if status == 200 and imgUrl.find("noimage") == -1:
                        urllib.request.urlretrieve(
                            imgUrl, "img/" + str(d['id']) + ".jpg")
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.reason)
            print(e.headers)


def load_dataframes():
    return pd.read_pickle(DUMP_FILE)


def main():

    print("[*] Crawling...")
    crawling()
    print("[+] Done")


if __name__ == "__main__":
    main()
