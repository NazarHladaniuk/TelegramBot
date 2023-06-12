from django.db import models
from datetime import date


class Task(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    due_date = models.DateField(default=date.today)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
