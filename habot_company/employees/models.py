from django.db import models
from django.utils import timezone
from datetime import date
class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateField(default=date.today)

    def __str__(self):
        return self.name
