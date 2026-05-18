from django.contrib import admin
from .models import Task, SubTask, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Выводим ID, Название, Статус, Дедлайн и Дату создания
    list_display = ('id', 'title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    # Выводим ID, Название, Основную задачу, Статус, Дедлайн и Дату создания
    list_display = ('id', 'title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at', 'task')
    search_fields = ('title', 'description')