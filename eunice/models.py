from django.db import models


# Create your models here.
class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    empID = models.CharField(max_length=20)
    dept = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=4)
    workID = models.CharField(max_length=20)
    job = models.CharField(max_length=20)
    section = models.CharField(max_length=20)
    team = models.CharField(max_length=20)
    process = models.CharField(max_length=20)
    jobType = models.CharField(max_length=20)
    employType = models.CharField(max_length=20)
    jobTitle = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    household = models.CharField(max_length=20)
    householdType = models.CharField(max_length=20)
    nation = models.CharField(max_length=20)
    political = models.CharField(max_length=20)
    firstWorkDate = models.CharField(max_length=20)
    education = models.CharField(max_length=20)
    degree = models.CharField(max_length=20)
    graduateDate = models.CharField(max_length=20)
    educationType = models.CharField(max_length=20)
    university = models.CharField(max_length=20)
    specialty = models.CharField(max_length=20)
    foreignLanguage = models.CharField(max_length=20)
    labor = models.CharField(max_length=20)
    contract = models.CharField(max_length=20)
    contractTime = models.CharField(max_length=20)
    contractStart = models.DateField()
    contractEnd = models.DateField()
    technicalTitle = models.CharField(max_length=20)
    technicalName = models.CharField(max_length=20)
    workerLevel = models.CharField(max_length=20)
    homeAddress = models.CharField(max_length=20)
    birthday = models.DateField()
    medicalResult = models.CharField(max_length=20)
    certificate = models.CharField(max_length=20)
    onboardDate = models.CharField(max_length=50)
    flag = models.CharField(max_length=10)


class SumDataBean(object):
    def __init__(self, deptName, gc, gl, jj, zj, zongji):
        self.deptName = deptName
        self.gc = gc
        self.gl = gl
        self.jj = jj
        self.zj = zj
        self.zongji = zongji
