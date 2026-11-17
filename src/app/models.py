from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    STATUS_CHOICES = (
        ("PLANNED", "планируется"),
        ("PROGRESS", "выполняется"),
        ("COMPLETED", "выполнено"),
        ("POSTPONED", "отложено"),
        ("ABANDONED", "брошено")
    )

    title: str = models.CharField(max_length=200)
    description: str = models.CharField(max_length=1000, blank=True, default="Описание отсутствует")
    status: str = models.CharField(choices=STATUS_CHOICES, default="PLANNED", max_length=12)
    owner: User = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at: datetime = models.DateTimeField(auto_now_add=datetime.now)
