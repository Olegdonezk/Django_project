from django.db import models

class StatusChoices(models.TextChoices):
    NEW = 'new', 'Новая'
    IN_PROGRESS = 'in_progress', 'В процессе'
    DONE = 'done', 'Выполнена'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ('name',)


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    categories = models.ManyToManyField(Category, related_name='tasks', verbose_name="Категории")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
        verbose_name="Статус"
    )
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'  # ОШИБКА БЫЛА ТУТ (стояло subtask)
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        unique_together = ('title',)


class SubTask(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название подзадачи")
    description = models.TextField(verbose_name="Описание подзадачи")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks', verbose_name="Основная задача")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,  # Переиспользуем статусы
        default=StatusChoices.NEW,
        verbose_name="Статус"
    )
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        unique_together = ('title',)