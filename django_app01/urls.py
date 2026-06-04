from django.urls import path

from .views import (
    hello,
    create_task,
    get_tasks,
    get_task,
    task_statistics,
    get_tasks_by_weekday,
    get_subtasks_filtered,
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


    path('tasks/by-weekday/', get_tasks_by_weekday),


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

    path('subtasks/filter/', get_subtasks_filtered),
]