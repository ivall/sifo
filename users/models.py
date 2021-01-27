from django.db import models


class User(models.Model):
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=255)
    account_type = models.CharField(max_length=5, default='user')  # user or admin
