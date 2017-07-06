from django.shortcuts import render

from .forms import *
from eunice import models


# Create your views here.

def employeeList(request):
    aList = models.Employee.objects.all()
    return render(request, 'index.html', {'dataList': aList})


def modify(request):
    aform = VideoForm()
    aform.opkind = 'modify'

    return render(request, 'employee.html', {'form': aform})


def delete(request):
    if request.method == 'POST':
        checkboxlist = request.POST.getlist('checkboxlist')
        if checkboxlist:
            idstring = ','.join(checkboxlist)
            models.Employee.objects.extra(where=['id IN (' + idstring + ')']).delete()

    aList = models.Employee.objects.all()

    return render(request, 'index.html', {'dataList': aList})


def search(request):
    if request.POST:
        sname = request.POST['searchName']
        kwargs = {}
        kwargs['empName'] = sname

    aList = models.Employee.objects.filter(name=sname)

    return render(request, 'index.html', {'dataList': aList})


def updateEmployee(request):
    if request.method == 'POST':
        aform = VideoForm(request.POST)
        opkind = request.GET('opkind')
        if aform.is_valid():
            ID = aform.cleaned_data['empID']
            staffname = aform.cleaned_data['name']
            bday = aform.cleaned_data['birthday']
            sexvalue = aform.cleaned_data['sex']
            wID = aform.cleaned_data['workID']
            job = aform.cleaned_data['job']
            dept = aform.cleaned_data['dept']
            if opkind == 'new':
                m = models.Employee.objects.create(empID=ID, dept=dept, job=job, workID=wID, name=staffname,
                                                   sex=sexvalue,
                                                   birthday=bday)
            else:
                id = aform.cleaned_data['id']
                employee = models.Employee.objects.filter(id=id).update(empID=ID, dept=dept, job=job, workID=wID,
                                                                        name=staffname, sex=sexvalue,
                                                                        birthday=bday)
    else:
        aform = VideoForm()

    return render(request, 'employee.html', {'form': aform})
