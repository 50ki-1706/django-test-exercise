from django.utils import timezone
from django.db import models


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)

    def is_overdue(self, dt: timezone.datetime) -> bool:
        if self.due_at is None:
            return False
        return self.due_at < dt
