from django.db.models.fields import TimeField
from os import truncate
from django.db import models

# Create your models here.

class User(models.Model):
    uid = models.PositiveIntegerField(primary_key=True)
    token = models.CharField(max_length=100, unique=True)
    expired_date = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    identity = models.CharField(max_length=10, default="visitor")
    is_read = models.BooleanField(default=False)