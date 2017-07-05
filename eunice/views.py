from django.shortcuts import render

from .forms import *
from eunice import models


# Create your views here.

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
        print(sname)

    aList = models.Employee.objects.filter(name=sname)

    return render(request, 'index.html', {'dataList': aList})


def sayHello(request):
    if request.method == 'POST':
        aform = VideoForm(request.POST)
        if aform.is_valid():
            ID = aform.cleaned_data['empID']
            staffname = aform.cleaned_data['name']
            bday = aform.cleaned_data['birthday']
            sexvalue = aform.cleaned_data['sex']
            wID = aform.cleaned_data['workID']
            job = aform.cleaned_data['job']
            dept = aform.cleaned_data['dept']

            m = models.Employee.objects.create(empID=ID, dept=dept, job=job, workID=wID, name=staffname, sex=sexvalue,
                                               birthday=bday)
    else:
        aform = VideoForm()

    aList = models.Employee.objects.all()

    return render(request, 'index.html', {'dataList': aList, 'form': aform})
