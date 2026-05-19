import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django_app01.models import Task, SubTask



task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=3)
)

print("Task created:", task)



subtask1 = SubTask.objects.create(
    task=task,
    title="Gather information",
    description="Find necessary information for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=2)
)

subtask2 = SubTask.objects.create(
    task=task,
    title="Create slides",
    description="Create presentation slides",
    status="New",
    deadline=timezone.now() + timedelta(days=1)
)

print("SubTask created:", subtask1)
print("SubTask created:", subtask2)



new_tasks = Task.objects.filter(status="New")

print("\nTasks with status 'New':")
for t in new_tasks:
    print(t.title, t.status)



expired_done_subtasks = SubTask.objects.filter(
    status="Done",
    deadline__lt=timezone.now()
)

print("\nExpired Done SubTasks:")
for st in expired_done_subtasks:
    print(st.title, st.deadline)



task.status = "In progress"
task.save()

print("\nUpdated task status:", task.status)



subtask1.deadline = timezone.now() - timedelta(days=2)
subtask1.save()

print("Updated deadline for Gather information")



subtask2.description = "Create and format presentation slides"
subtask2.save()

print("Updated description for Create slides")



task.delete()

print("\nTask and all subtasks deleted")