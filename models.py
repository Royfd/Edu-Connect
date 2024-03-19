from django.db import models
from django.contrib.auth.models import User


class profile1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)


class Message(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')
    resume = models.FileField(upload_to="SMS/static")
    text = models.TextField()


class Doubt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class Assignment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="SMS/static")
