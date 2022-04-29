from concurrent.futures.process import _python_exit
from os import stat
from statistics import mode
from django.db import models

# Create your models here.

class Volunteer(models.Model):
    id = models.CharField(max_length=4,primary_key=True)
    firstname = models.CharField(max_length=50,null=False)
    lastname = models.CharField(max_length=50,null=False)
    phone = models.CharField(max_length=10,null=False)
    email = models.CharField(max_length=50,null=False)
    address = models.CharField(max_length=70,null=False)
    city = models.CharField(max_length=20,null=False)
    state = models.CharField(max_length=20,null=False)
    status = models.CharField(max_length=10,null=False)

    def __str__(self):
        return self.id
