from .models import Store, Review, Menu, User, Account, Bhour
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as u
from django.contrib.auth.hashers import make_password


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
            "branch",
            "area",
            "tel",
            "address",
            "latitude",
            "longitude",
            "reviewCnt",
            "category_list",
            "image",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",  # 리뷰 고유번호
            "store",  # 음식점 고유번호
            "user",  # 유저 고유번호
            "score",  # 평점
            "content",  # 리뷰 내용
            "reg_time",  # 리뷰 등록 시간
        )


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id",  # 메뉴 고유번호
            "store",  # 음식점 고유번호
            "menu_name",  # 음식 이름
            "price"  # 음식 가격
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",  # 유저 고유 번호
            "gender",  # 유저 성별
            "age"  # 유저 나이
        ]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = u
        fields = ('id', 'username', 'email', 'password','is_superuser')
        extra_kwargs = {"password": {"write_only": True}}

# 회원가입


class BhourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bhour
        fields = '__all__'


class UserCreationSerializer(serializers.ModelSerializer):
    user = AccountSerializer(required=True)

    class Meta:
        model = Account
        fields = ('user', "age", "gender")

    def create(self, validated_data):
        user_data = validated_data['user']
        user = u.objects.create_user(
            user_data["username"], user_data["email"], user_data["password"],)
        account, created = Account.objects.update_or_create(
            user=user, age=validated_data['age'], gender=validated_data['gender'])
        return user

    def update(self, instance, validated_data):
        user_data = validated_data['user']
        user = u.objects.get(pk=instance)
        user.username = user_data["username"]
        user.email = user_data["email"]
        user.password = make_password(user_data["password"])
        user.save()
        account = Account.objects.get(user_id=instance)
        account.user = user
        account.age = validated_data['age']
        account.gender = validated_data['gender']
        account.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    user = AccountSerializer(required=True)

    class Meta:
        model = Account
        fields = ('user', 'age', 'gender')


# 로그인
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            "Unable to log in with provided credentials.")
