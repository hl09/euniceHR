from django.db import models


# Create your models here.
class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    empID = models.CharField(max_length=20)
    dept = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    workID = models.CharField(max_length=20)
    job = models.CharField(max_length=20)
    sex = models.CharField(max_length=4)
    birthday = models.DateField()
