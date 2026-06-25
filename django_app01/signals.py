from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Task, StatusChoices


@receiver(pre_save, sender=Task)
def task_status_notification(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_task = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    if old_task.status == instance.status:
        return

    if instance.status == StatusChoices.DONE:
        subject = "Task closed"
        message = (
            f"Task '{instance.title}' has been completed."
        )
    else:
        subject = "Task status changed"
        message = (
            f"Task '{instance.title}' status changed "
            f"from '{old_task.get_status_display()}' "
            f"to '{instance.get_status_display()}'."
        )

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[instance.owner.email],
        fail_silently=False,
    )