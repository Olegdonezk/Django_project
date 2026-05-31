from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer

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



# Create your views here.
def hello(request):
    return HttpResponse("Hello, Oleg!")