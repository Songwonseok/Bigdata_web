from django.conf.urls import url
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter(trailing_slash=False)
router.register(r"stores", views.StoreViewSet, basename="stores")
router.register(r"review", views.ReviewViewSet, basename="review")
router.register(r"menu", views.MenuViewSet, basename="menu")
router.register(r"user", views.UserViewSet, basename="user")

router.register(r"storeoption", views.StoreOprionViewSet, basename="option")
router.register(r"ad", views.AdminReviewAPI, basename="adminReview")
router.register(r"adminuser", views.AdminUserAPI, basename="adminUser")
router.register(r"bhour", views.BhourViewSet, basename="bhour")

urlpatterns = [
    path('auth/join/', views.RegistrationAPI.as_view(), name='join'),
    path('auth/login/', views.LoginAPI.as_view(), name='login'),
    path('auth/user/auth/', views.UserAPI.as_view(), name='check'),
    path('admin/count',views.AdminCountAPI.as_view(), name="admin_count"),
    path('admin/user/change', views.AdminAccountAPI.as_view(), name="admin_acc_change"),
    path('admin/review/change', views.AdminReviewChangeAPI.as_view(), name="admin_review_change"),
    path('users/change',views.UserAccountChangeAPI.as_view(), name="user_account_change")
]


urlpatterns += router.urls
