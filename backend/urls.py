from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "backend"

# API router
router = routers.DefaultRouter()
router.register(r'crafts', views.CraftViewSet)

urlpatterns = [
    # Основные страницы
    path("", views.home_view, name="home"),
    path("crafts/", views.craft_list_view, name="crafts"),
    path("crafts/<int:pk>/", views.craft_detail_view, name="craft_detail"),
    path("crafts/<int:pk>/leave/", views.leave_request_view, name="leave_request"),
    path("map/", views.map_view, name="map"),

    # Авторизация
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # API
    path("api/", include(router.urls)),
]
