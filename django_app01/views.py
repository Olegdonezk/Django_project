from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task, SubTask
from .serializers import (
    TaskSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@api_view(['GET'])
def task_statistics(request):
    return Response({
        "total_tasks": Task.objects.count(),
        "tasks_by_status": list(
            Task.objects.values('status').annotate(count=Count('id'))
        ),
        "overdue_tasks": Task.objects.filter(
            deadline__lt=timezone.now()
        ).count()
    })


@api_view(['GET'])
def get_tasks_by_weekday(request):
    weekday = request.GET.get('weekday')

    tasks = Task.objects.all()

    if weekday:
        weekdays = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6,
        }

        weekday_num = weekdays.get(weekday.lower())

        if weekday_num is not None:
            tasks = [
                task for task in tasks
                if task.deadline.weekday() == weekday_num
            ]

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)



class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class SubTaskDetailUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


def hello(request):
    return HttpResponse("Hello, Oleg!")