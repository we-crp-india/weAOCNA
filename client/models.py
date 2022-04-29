from django.db import models

class Resque(models.Model):
    id = models.CharField(max_length=21,primary_key=True)
    firstname = models.CharField(max_length=50,null=False)
    lastname = models.CharField(max_length=50,null=False)
    email = models.CharField(max_length=100,null=False)
    phone = models.CharField(max_length=10,null=False)
    addrs = models.CharField(max_length=200,null=False)
    breed = models.CharField(max_length=20,null=False)
    vaccination = models.CharField(max_length=3,null=False,default="no")
    reason = models.CharField(max_length=100,null=True)
    condition = models.CharField(max_length=10,null=False,default="Good")
    date = models.CharField(max_length=19,null=False)
    status = models.CharField(max_length=20,null=False)
    vol = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.id
