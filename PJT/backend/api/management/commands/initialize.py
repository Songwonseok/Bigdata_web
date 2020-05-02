from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from backend import settings
from api import models
from django.contrib.auth.models import User as u
from sqlalchemy import create_engine
import pymysql
import MySQLdb
import configparser
import math


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = str(DATA_DIR / "dump.pkl")

    def _load_dataframes(self):
        try:
            data = pd.read_pickle(Command.DATA_FILE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data

    def _initialize(self):
        """
        Sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] Loading data...")
        dataframes = self._load_dataframes()

        # print("[*] Initializing stores...")
        # models.Store.objects.all().delete()
        # stores = dataframes["stores"]
        # stores_bulk = [
        #     models.Store(
        #         id=store.id,
        #         store_name=store.store_name,
        #         branch=store.branch,
        #         area=store.area,
        #         tel=store.tel,
        #         address=store.address,
        #         latitude=store.latitude,
        #         longitude=store.longitude,
        #         category=store.category,
        #         reviewCnt=store.reviewCnt,
        #         image=store.image
        #     )
        #     for store in stores.itertuples()
        # ]
        # models.Store.objects.bulk_create(stores_bulk)
        # print("[+] Done")

        # print("[*] Initializing users...")
        # models.User.objects.all().delete()
        # u.objects.all().delete()
        # models.Account.objects.all().delete()
        # users = dataframes["users"]
        # users_bulk = []
        # accounts_bulk = []
        # auth_bulk = []
        # for user in users.itertuples():
        #     users_bulk.append(models.User(
        #         id=user.id,
        #         gender=user.gender,
        #         age=user.age,
        #     ))
        #     auth_bulk.append(u(
        #         id=user.id,
        #         password='anonymous123!',
        #         is_superuser=0,
        #         username='anonymous' + str(user.id),
        #         first_name='',
        #         last_name='',
        #         email='',
        #         is_staff=0,
        #         is_active=0
        #     ))
        # models.User.objects.bulk_create(users_bulk)
        # u.objects.bulk_create(auth_bulk)

        # print("[+] Done")
        # print("[*] Initializing accounts...")
        # accounts_bulk = [
        #     models.Account(
        #         id=index+1,
        #         gender=user.gender,
        #         age=user.age,
        #         user_id=user.id
        #     )
        #     for index, user in enumerate(users.itertuples())
        # ]
        # models.Account.objects.bulk_create(accounts_bulk)
        # print("[+] Done")

        print("[*] Initializing menus...")
        models.Menu.objects.all().delete()
        menus = dataframes["menus"]
        menus_bulk = [
            models.Menu(
                id=menu.id,
                store_id=menu.store,
                menu_name=menu.menu_name,
                price=menu.price if math.isnan(
                    float(menu.price)) == False else 0,
            )
            for menu in menus.itertuples()
        ]
        models.Menu.objects.bulk_create(menus_bulk)
        print("[+] Done")

        print("[*] Initializing reviews...")
        models.Review.objects.all().delete()
        reviews = dataframes["reviews"]
        reviews_bulk = [
            models.Review(
                id=index+1,
                store_id=review.store,
                user_id=review.user,
                score=review.score,
                content=review.content,
                reg_time=review.reg_time,
            )
            for index, review in enumerate(reviews.itertuples())
        ]
        models.Review.objects.bulk_create(reviews_bulk)
        print("[+] Done")

        print("[*] Initializing bhours...")
        models.Bhour.objects.all().delete()
        bhours = dataframes["bhours"]
        bhours_bulk = [
            models.Bhour(
                id=index+1,
                store_id=bhour.store,
                week_type=bhour.week_type,
                bhour_type=bhour.type,
                mon=bhour.mon if math.isnan(float(bhour.mon)) == False else 0,
                tue=bhour.tue if math.isnan(float(bhour.tue)) == False else 0,
                wed=bhour.wed if math.isnan(float(bhour.wed)) == False else 0,
                thu=bhour.thu if math.isnan(float(bhour.thu)) == False else 0,
                fri=bhour.fri if math.isnan(float(bhour.fri)) == False else 0,
                sat=bhour.sat if math.isnan(float(bhour.sat)) == False else 0,
                sun=bhour.sun if math.isnan(float(bhour.sun)) == False else 0,
                start_time=bhour.start_time,
                end_time=bhour.end_time,
                etc=bhour.etc
            )
            for index, bhour in enumerate(bhours.itertuples())
        ]
        models.Bhour.objects.bulk_create(bhours_bulk)
        print("[+] Done")

    def handle(self, *args, **kwargs):
        self._initialize()
