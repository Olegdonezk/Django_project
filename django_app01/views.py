from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task, SubTask, Category
from .serializers import (
    TaskSerializer,
    SubTaskSerializer,
    CategorySerializer,
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        count = category.task_set.count()
        return Response({'category': category.name, 'task_count': count})

    def perform_destroy(self, instance):
        instance.delete()


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
    """Возвращает общую статистику по задачам"""
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

        weekdays_django = {
            'sunday': 1,
            'monday': 2,
            'tuesday': 3,
            'wednesday': 4,
            'thursday': 5,
            'friday': 6,
            'saturday': 7,
        }

        weekday_num = weekdays_django.get(weekday.lower())

        if weekday_num is not None:
            tasks = tasks.filter(deadline__week_day=weekday_num)
        else:
            return Response(
                {"error": "Неверный день недели. Используйте monday, tuesday и т.д."},
                status=status.HTTP_400_BAD_REQUEST
            )

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


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer



def hello(request):
    return HttpResponse("Hello, Oleg!")