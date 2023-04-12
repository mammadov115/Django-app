from django.db import models

# Create your models here.

class Account(models.Model):
    login = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=50)
    followers = models.IntegerField()
    following = models.IntegerField()

    def __str__(self):
        return self.username
    