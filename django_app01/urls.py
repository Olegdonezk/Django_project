from django.urls import path

from .views import (
    hello,
    create_task,
    get_tasks,
    get_task,
    task_statistics,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

urlpatterns = [
    path('', hello),

    # Task
    path('tasks/create/', create_task),
    path('tasks/', get_tasks),
    path('tasks/<int:task_id>/', get_task),
    path('tasks/statistics/', task_statistics),

    # SubTask
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