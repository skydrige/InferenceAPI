from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat_Session(models.Model):
    username = models.CharField(max_length=30)
    session_id = models.CharField(max_length=100, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Chat_Messages(models.Model):
    session = models.CharField(max_length=100)
    username = models.CharField(max_length=30)
    message_id = models.CharField(max_length=50, primary_key=True)
    user = models.CharField(max_length=5000)
    model = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)


class test_session(models.Model):
    username = models.CharField(max_length=100)
    message_id = models.CharField(max_length=100, primary_key=True)
    user = models.CharField(max_length=1000)
    model = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message_id
