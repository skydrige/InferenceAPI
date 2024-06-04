from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=100)
#     username = models.CharField(max_length=100, primary_key=True)
#     password = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#
#     def __str__(self):
#         return User(self.name, self.username, self.email)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, primary_key=True)


class Messages(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    message_id = models.CharField(max_length=100, primary_key=True)
    user = models.CharField(max_length=1000)
    model = models.CharField(max_length=1000)
    timestamp = models.DateTimeField()


class test_session(models.Model):
    username = models.CharField(max_length=100)
    message_id = models.CharField(max_length=100, primary_key=True)
    user = models.CharField(max_length=1000)
    model = models.CharField(max_length=1000)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.message_id
