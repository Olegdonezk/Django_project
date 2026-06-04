from django.utils import timezone
from rest_framework import serializers
from .models import Task, SubTask, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

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
    class Meta:
        model = SubTask
        fields = "__all__"


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
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