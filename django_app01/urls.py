from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    hello,
    TestAPIView,
    TaskViewSet,
    SubTaskViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'subtasks', SubTaskViewSet, basename='subtasks')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', hello),
    path('test/', TestAPIView.as_view(), name='test'),
    path('', include(router.urls)),
]