from django.db.models import Count
from knox.models import AuthToken
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from . import models, serializers
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .algo import ItemBased, UserBased, TF_IDF_Recommend_Store
from django.contrib.auth.models import User as u
import random


class SmallPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 50


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StoreSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        store_id = self.request.query_params.get("id", "")
        name = self.request.query_params.get("name", "")
        category = self.request.query_params.get("category", "")
        address = self.request.query_params.get("address", "")
        reviewCnt = self.request.query_params.get("count", "")
        reviewCnt = int(reviewCnt) if reviewCnt != "" else - 1
        user_id = self.request.query_params.get("user", "")
        if store_id != "":
            recommStore = self.request.query_params.get("recomm", "")
            if recommStore != "":
                list = TF_IDF_Recommend_Store.get_Similar_Store(
                    recommStore)
                queryset = (
                    models.Store.objects.all().filter(id__in=list).order_by("id")
                )
            else:
                queryset = (
                    models.Store.objects.all().filter(id=store_id).order_by("id")
                )
        else:
            print("야호")
            if user_id != "":
                try:
                    list = UserBased.train(user_id, 5)
                except ValueError as v:
                    max = models.Store.objects.count()
                    list = [random.randint(0, max) for r in range(10)]
                queryset = (
                    models.Store.objects.all().filter(id__in=list).order_by("id")
                )
            else:
                queryset = (
                    models.Store.objects.all().filter(store_name__contains=name,
                                                      category__contains=category,
                                                      address__contains=address,
                                                      reviewCnt__gt=reviewCnt).order_by("id")
                )
        return queryset


class StoreOprionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    pagination_class = SmallPagination

    def get_queryset(self):
        name = self.request.query_params.get("name", "")
        count = self.request.query_params.get("count", "")
        print(name)
        print(count)
        # store_count = models.Review.objects.distinct().values("store_id").annotate(store_count=Count("store_id")).filter(store_count__gt=count)
        store_count = models.Review.objects.annotate(
            cnt=Count('store')).filter(cnt__gt=count)
        #queryset = models.Store.objects.filter(id__in = store_count).filter(store_name__contains=name)
        # queryset = (models.Store.objects.raw('SELECT * FROM api_swtore WHERE id In ( SELECT store FROM api_review GROUP BY store HAVING COUNT(*) > {0}) and store_name LIKE {1};'.format(name,count)))
        return store_count


class BhourViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BhourSerializer
    pagenation_class = SmallPagination

    def get_queryset(self):
        store = self.request.query_params.get("store", "")
        if store != "":
            queryset = (models.Bhour.objects.all().filter(store_id=store))
        else:
            queryset = models.Bhour.objects.all()

        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        store = self.request.query_params.get("id", "")
        content = self.request.query_params.get("content", "")
        if store != "":
            queryset = (
                models.Review.objects.all().filter(
                    store=store).order_by("-id")
            )
        else:
            queryset = (
                models.Review.objects.all().filter(content__contains=content).order_by("-id")
            )
        return queryset
        


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MenuSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        name = self.request.query_params.get("name", "")
        store = self.request.query_params.get("store", "")

        if store != "":
            queryset = (models.Menu.objects.all().filter(
                menu_name__contains=name, store=store).order_by("id"))
        else:
            queryset = (models.Menu.objects.all().filter(
                menu_name__contains=name).order_by("id"))

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserCreationSerializer
    pagination_class = SmallPagination
    queryset = models.Account.objects.all()

    def get_queryset(self):
        store_id = self.request.query_params.get("store", "")
        user_id = self.request.query_params.get("user", "")
        if store_id != "":
            try:
                list = ItemBased.train(store_id, 10)
                queryset = (
                    self.queryset.filter(user_id__in=list).order_by("-id")
                )
            except ValueError as v:
                max = models.Account.objects.all().count()
                list = [random.randint(0, max) for r in range(10)]
                queryset = (
                    self.queryset.filter(id__in=list).order_by("-id")
                )

            return queryset
        else:
            if user_id != "":
                queryset = (
                    self.queryset.filter(user_id=user_id).order_by("-id")
                )
                print(queryset)
            else:
                queryset = (
                    self.queryset.order_by("id")
                )

            return queryset

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        tmp = request.data['user']['username']
        request.data['user']['username'] = 'anonymous-1'
        serializer = self.get_serializer(pk, data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        request.data['user']['username'] = tmp
        serializer = self.get_serializer(pk, data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": serializers.AccountSerializer(
                user, context=self.get_serializer_context()
            ).data,
        })
        return Response

    def destroy(self, request, pk=None):
        user = u.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializer

    def post(self, req, *args, **kwargs):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": serializers.AccountSerializer(
                user, context=self.get_serializer_context()
            ).data,
            "token": token
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = serializers.LoginUserSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response(
            {
                "user": serializers.AccountSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": token
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        user = self.request.query_params.get("user", "")

        queryset = (models.Account.objects.all().filter(
                user_id=user))
                
        return queryset

class AdminCountAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user_count = models.User.objects.count()
        store_count = models.Store.objects.count()
        review_count = models.Review.objects.count()
        return Response({
            "userCount": user_count,
            "storeCount": store_count,
            "reviewCount": review_count
        })

class AdminReviewAPI(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = SmallPagination
    def get_queryset(self):
          queryset = models.Review.objects.all().order_by("reg_time")
          return queryset

class AdminUserAPI(viewsets.ModelViewSet):

    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        queryset = u.objects.all().exclude(username__contains="anony")
        return queryset


class AdminAccountAPI(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializer
    def post(self, request, *args, **kwargs):
        print(request.data)
        try:
            user = u.objects.get(username=request.data['username'])
            user.is_superuser = not user.is_superuser
            user.save()
        except u.DoesNotExist:
            print("error")
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminReviewChangeAPI(generics.GenericAPIView):
    serializer_class = serializers.ReviewSerializer
    def post(self, request, *args, **kwargs):
        print("hello")
        print(request.data)
        try:
            queryset = models.Review.objects.get(id=request.data['id'])
            queryset.content = "블라인드 처리 되었습니다."
            queryset.save()
        except u.DoesNotExist:
            print("error")
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserAccountChangeAPI(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        try:
            user = u.objects.get(username=request.data['user']['username'])
            user.username = request.data['user']['username']
            
            user.email = request.data['user']['email']
            
            queryset = models.Account.objects.get(user_id=user.id)
            
            queryset.age = request.data['age']
            
            queryset.gender = request.data['gender']
            

            queryset.save()
            user.save()

        except u.DoesNotExist:
            print("error")
        return Response(status=status.HTTP_204_NO_CONTENT)