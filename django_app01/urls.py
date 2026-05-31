from django.urls import path
from .views import hello


from django.urls import path

from .views import (
    hello,
    create_task,
    get_tasks,
    get_task,
    task_statistics
)

urlpatterns = [
    path('', hello),

    path('tasks/create/', create_task),
    path('tasks/', get_tasks),
    path('tasks/<int:task_id>/', get_task),
    path('tasks/statistics/', task_statistics),
]