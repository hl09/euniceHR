from django.shortcuts import render ,HttpResponse ,HttpResponseRedirect,render_to_response
from .forms import *
from eunice import models
import json



# Create your views here.

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, (datetime,date,)):
                 return obj.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return json.JSONEncoder.default(self, obj)
        except Exception as e:
            print(e)


def employeeList(request):
    aList = models.Employee.objects.all()
    return render(request, 'index.html', {'dataList': aList})

def showgrid(request):
    return render(request, 'a.html')

def weekReport(request):
    aList = models.Employee.objects.all()
    dataList = []
    for aItem in aList:
        dataList.append({"empID": aItem.empID, "dept": aItem.dept, "name": aItem.name, "job": aItem.job})


    eaList_len = json.dumps(len(dataList))
    json_data_list = {'rows':dataList,'total':eaList_len}
    easyList = json.dumps(json_data_list, cls=CJsonEncoder)
    return HttpResponse(easyList)

def statistical(request):
    depts = ['安监室', '财务', '技术', '商务', '制造', '制造-物流', '质保', '综合办']
    beanList = []
    sgc = 0
    sgl = 0
    sjj = 0
    szj = 0
    if request.method == 'POST':
        # 按部门进行循环统计
        for dept in depts:
            query = models.Employee.objects.filter(dept=dept)
            zongji = query.count()
            # 按四大类别进行统计
            gc = query.filter(jobType='工程技术人员').count()
            gl = query.filter(jobType='管理人员').count()
            jj = query.filter(jobType='间接生产工人').count()
            zj = query.filter(jobType='直接生产工人').count()

            aBean = models.SumDataBean(dept, gc, gl, jj, zj, zongji)
            beanList.append(aBean)
            sgc = sgc + gc
            sgl = sgl + gl
            sjj = sjj + jj
            szj = szj + zj
        sumBean = models.SumDataBean('总计', sgc, sgl, sjj, szj, sgc + sgl + sjj + szj)
        beanList.append(sumBean)
    return render(request, 'sumpage.html', {'depts': depts, 'beanList': beanList})


def showModify(request):
    opkind = request.GET.get('opkind')
    flag = opkind
    if opkind == 'm':
        id = request.GET.get('id')
        employee = models.Employee.objects.get(id=id)

        empID = employee.empID
        name = employee.name
        dept = employee.dept
        job = employee.job
        birthday = employee.birthday
        workID = employee.workID
        sex = employee.sex
        onboardDate = employee.onboardDate
        if employee:
            aform = VideoForm(
                {'name': name, 'dept': dept, 'opkind': opkind, 'empID': empID, 'birthday': birthday, 'job': job,
                 'workID': workID, 'onboardDate': onboardDate, 'sex': sex})
    else:
        aform = VideoForm()

    return render(request, 'employee.html', {'form': aform})


def saveEmployee(request):
    if request.method == 'POST':
        aform = VideoForm(request.POST)
        if aform.is_valid():
            opkind = aform.cleaned_data['opkind']

            if opkind == 'm':
                empID = aform.cleaned_data['empID']
                employee = models.Employee.objects.get(empID=empID)
            else:
                employee = models.Employee()

            employee.workID = aform.cleaned_data['workID']
            employee.job = aform.cleaned_data['job']
            employee.birthday = aform.cleaned_data['birthday']
            employee.sex = aform.cleaned_data['sex']
            employee.dept = aform.cleaned_data['dept']
            employee.name = aform.cleaned_data['name']
            employee.onboardDate = aform.cleaned_data['onboardDate']
            employee.save()

        aList = models.Employee.objects.all()
        return render(request, 'index.html', {'dataList': aList})


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
        kwargs = {}

        sname = request.POST['searchName']
        sID = request.POST['searchID']
        sDept = request.POST['searchDept']

        if sname:
            kwargs['name'] = sname
        if sID:
            kwargs['workID'] = sID
        if sDept:
            kwargs['dept'] = sDept

        aList = models.Employee.objects.filter(**kwargs)
        # aList = models.Employee.objects.filter(Q(name__contains=sname) | Q(workID=sID))

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
