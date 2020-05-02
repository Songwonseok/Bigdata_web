from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User as u
from django.db.models.signals import post_save
from django.dispatch import receiver


class Store(models.Model):
    id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=50, null=True)
    tel = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(max_length=10, null=True)
    longitude = models.FloatField(max_length=10, null=True)
    category = models.CharField(max_length=200, null=True)
    reviewCnt = models.IntegerField(default=0)
    image = models.CharField(max_length=200, null=True)
    @property
    def category_list(self):
        return self.category.split("|") if self.category else []


class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=190, null=True)
    price = models.FloatField(null=True)


class Bhour(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE)
    bhour_type = models.PositiveSmallIntegerField(null=True)
    week_type = models.PositiveSmallIntegerField(null=True)
    mon = models.PositiveSmallIntegerField(null=True)
    tue = models.PositiveSmallIntegerField(null=True)
    wed = models.PositiveSmallIntegerField(null=True)
    thu = models.PositiveSmallIntegerField(null=True)
    fri = models.PositiveSmallIntegerField(null=True)
    sat = models.PositiveSmallIntegerField(null=True)
    sun = models.PositiveSmallIntegerField(null=True)
    start_time = models.CharField(max_length=20, null=True)
    end_time = models.CharField(max_length=20, null=True)
    etc = models.CharField(max_length=180, null=True)


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)


class Account(models.Model):
    user = models.OneToOneField(u, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)

    def __str__(self):
        return str(self.user) + ", " + self.gender + ", " + str(self.age)


@receiver(post_save, sender=User)
def create_user_Account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_Account(sender, instance, **kwargs):
    instance.account.save()





class Review(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE)
    user = models.ForeignKey(u, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    content = models.TextField(null=True)
    reg_time = models.DateTimeField(auto_now_add=True)
