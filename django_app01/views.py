from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, SubTask, Category
from .serializers import (
    TaskSerializer,
    SubTaskSerializer,
    CategorySerializer,
)
from .permissions import IsOwnerOrReadOnly


class TestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "JWT работает",
            "user": request.user.username
        })


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def my(self, request):
        serializer = self.get_serializer(
            Task.objects.filter(owner=request.user),
            many=True
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        return Response({
            "total_tasks": Task.objects.count(),
            "tasks_by_status": list(
                Task.objects.values('status').annotate(count=Count('id'))
            ),
            "overdue_tasks": Task.objects.filter(
                deadline__lt=timezone.now()
            ).count()
        })


class SubTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubTaskSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()

        return Response({
            "category": category.name,
            "task_count": category.tasks.count()
        })

    def perform_destroy(self, instance):
        instance.delete()


def hello(request):
    return HttpResponse("Hello, Oleg!")