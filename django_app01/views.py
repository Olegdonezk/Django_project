from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Task, SubTask
from .serializers import (
    TaskSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)

@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    serializer = TaskSerializer(task)
    return Response(serializer.data)


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


class SubTaskPagination(PageNumberPagination):
    page_size = 5


class SubTaskListCreateView(APIView):

    def get(self, request):
        subtasks = SubTask.objects.all().order_by('-created_at')

        paginator = SubTaskPagination()
        result_page = paginator.paginate_queryset(subtasks, request)

        serializer = SubTaskSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SubTaskDetailUpdateDeleteView(APIView):

    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)

        serializer = SubTaskCreateSerializer(subtask, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()

        return Response(
            {"message": "Подзадача удалена"},
            status=status.HTTP_204_NO_CONTENT
        )



@api_view(['GET'])
def get_subtasks_filtered(request):
    task_title = request.GET.get('task')
    status_filter = request.GET.get('status')

    subtasks = SubTask.objects.all().order_by('-created_at')

    if task_title:
        subtasks = subtasks.filter(task__title__icontains=task_title)

    if status_filter:
        subtasks = subtasks.filter(status=status_filter)

    paginator = SubTaskPagination()
    result_page = paginator.paginate_queryset(subtasks, request)

    serializer = SubTaskSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


def hello(request):
    return HttpResponse("Hello, Oleg!")