from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    hello,
    task_statistics,
    get_tasks_by_weekday,
    TaskListCreateView,
    TaskDetailView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', hello),

    # Tasks CRUD
    path(
        'tasks/',
        TaskListCreateView.as_view(),
        name='task-list-create'
    ),
    path(
        'tasks/<int:pk>/',
        TaskDetailView.as_view(),
        name='task-detail'
    ),

    # Statistics (оставляем как есть)
    path(
        'tasks/statistics/',
        task_statistics,
        name='task-statistics'
    ),

    # Дополнительный эндпойнт
    path(
        'tasks/by-weekday/',
        get_tasks_by_weekday,
        name='tasks-by-weekday'
    ),

    # SubTasks CRUD
    path(
        'subtasks/',
        SubTaskListCreateView.as_view(),
        name='subtask-list-create'
    ),
    path(
        'subtasks/<int:pk>/',
        SubTaskDetailUpdateDeleteView.as_view(),
        name='subtask-detail-update-delete'
    ),
]

urlpatterns += router.urls