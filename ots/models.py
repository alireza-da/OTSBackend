import random
import string

from django.contrib.auth.models import User
from django.db import models


class Session(models.Model):
    name = models.TextField(max_length=250)
    start_date = models.DateTimeField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=25, unique=True)


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    role = models.CharField(max_length=250)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    content = models.TextField()
    fullname = models.TextField(max_length=255, default="Participant")


