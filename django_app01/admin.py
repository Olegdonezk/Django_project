from django.contrib import admin
from .models import Task, SubTask, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.action(description='Mark selected subtasks as Done')
def mark_as_done(modeladmin, request, queryset):
    queryset.update(status='Done')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Выводим ID, Название, Статус, Дедлайн и Дату создания
    list_display = ('id', 'title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)

    inlines = [SubTaskInline]

    def short_title(self, obj):
        if len(obj.title) > 10:
            return f'{obj.title[:10]}...'
        return obj.title

    short_title.short_description = 'Title'

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    # Выводим ID, Название, Основную задачу, Статус, Дедлайн и Дату создания
    list_display = ('id', 'title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at', 'task')
    search_fields = ('title', 'description')

    actions = [mark_as_done]