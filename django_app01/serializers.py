import re

from django.utils import timezone
from rest_framework import serializers
from .models import Task, SubTask, Category
from django.contrib.auth.password_validation import validate_password

from .models import User

from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"]
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials"
            )

        attrs["user"] = user
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Username already exists'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Email already exists'
            )
        return value

    def validate_password(self, value):
        validate_password(value)

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                'Password must contain uppercase letter'
            )

        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                'Password must contain digit'
            )

        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )


class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_deleted', 'deleted_at', 'task_count']
        read_only_fields = ['is_deleted', 'deleted_at']

    def get_task_count(self, obj):
        return obj.tasks.count()


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def create(self, validated_data):
        name = validated_data.get("name")

        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                {"name": "Категория с таким названием уже существует."}
            )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get("name")

        if (
            name
            and Category.objects.filter(name=name)
            .exclude(id=instance.id)
            .exists()
        ):
            raise serializers.ValidationError(
                {"name": "Категория с таким названием уже существует."}
            )

        return super().update(instance, validated_data)



class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = SubTask
        fields = "__all__"


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Дедлайн не может быть в прошлом."
            )
        return value


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"