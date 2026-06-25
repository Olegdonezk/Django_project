from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken




from .models import Task, SubTask, Category
from .serializers import (
    TaskSerializer,
    SubTaskSerializer,
    CategorySerializer,
)
from .permissions import IsOwnerOrReadOnly

from .serializers import RegisterSerializer
from .serializers import LoginSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax"
        )

        return response

class RefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "No refresh token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = RefreshToken(refresh_token)

        return Response(
            {"access": str(token.access_token)},
            status=status.HTTP_200_OK
        )

class LogoutView(APIView):

    def post(self, request):

        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        response = Response(
            {"messsage": "Logget out"}
        )

        response.delete_cookie(
            key="access_token",
        )

        response.delete_cookie(
            key="refresh_token",
        )

        return response



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