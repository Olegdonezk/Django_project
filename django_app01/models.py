from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = 'New', 'New'
        IN_PROGRESS = 'In progress', 'In progress'
        PENDING = 'Pending', 'Pending'
        BLOCKED = 'Blocked', 'Blocked'
        DONE = 'Done', 'Done'

    title = models.CharField(max_length=200, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    categories = models.ManyToManyField(Category, related_name="tasks", verbose_name="Категории")
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
        # Уникальность названия для конкретной даты (используем дату из created_at или deadline)
        # В данном случае, так как created_at создается автоматически, логичнее проверять по ней
        unique_together = ('title', 'created_at')
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class SubTask(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название подзадачи")
    description = models.TextField(verbose_name="Описание подзадачи")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks", verbose_name="Основная задача")
    status = models.CharField(
        max_length=20,
        choices=Task.StatusChoices.choices,
        default=Task.StatusChoices.NEW,
        verbose_name="Статус"
    )
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Подзадача"
        verbose_name_plural = "Подзадачи"
