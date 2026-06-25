from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    hello,
    TestAPIView,
    TaskViewSet,
    SubTaskViewSet,
    CategoryViewSet,
    RegisterView,
    LoginView,
    RefreshView,
    LogoutView

)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'subtasks', SubTaskViewSet, basename='subtasks')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', hello),
    path('test/', TestAPIView.as_view(), name='test'),
    path('', include(router.urls)),

    path("register/", RegisterView.as_view(), name="register"),

    path("login/", LoginView.as_view(), name="login"),

    path("refresh/", RefreshView.as_view(), name="refresh"),

    path("logout/", LogoutView.as_view(), name="logout"),
]