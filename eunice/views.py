from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from .forms import *
from eunice import models
import json
import win32com.client as wc
import pythoncom


# Create your views here.

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, (datetime, date,)):
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
    pythoncom.CoInitialize()
    excel_app = wc.Dispatch('Excel.Application')
    workbook = excel_app.Workbooks.open(r'D:\pythonTraining\euniceHR\static\1.xlsx')

    i = 1
    for aItem in aList:
        i = i + 1
        dataList.append({"empID": aItem.empID, "dept": aItem.dept, "name": aItem.name, "job": aItem.job})
        workbook.Worksheets('Sheet1').Cells(i, 1).Value = i - 1
        workbook.Worksheets('Sheet1').Cells(i, 1).BorderAround(1, 4)

        workbook.Worksheets('Sheet1').Cells(i, 2).Value = aItem.dept
        workbook.Worksheets('Sheet1').Cells(i, 2).BorderAround(1, 4)

        workbook.Worksheets('Sheet1').Cells(i, 3).Value = aItem.name
        workbook.Worksheets('Sheet1').Cells(i, 3).BorderAround(1, 4)

        workbook.Worksheets('Sheet1').Cells(i, 4).Value = aItem.job
        workbook.Worksheets('Sheet1').Cells(i, 4).BorderAround(1, 1)

    workbook.SaveAs(r'D:\aa.xlsx')
    excel_app.Application.Quit()

    eaList_len = json.dumps(len(dataList))
    json_data_list = {'rows': dataList, 'total': eaList_len}
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
        mobile = employee.mobile
        household = employee.household
        contract = employee.contract
        contractTime = employee.contractTime
        contractStart = employee.contractStart
        contractEnd = employee.contractEnd

        if employee:
            aform = VideoForm(
                {'name': name, 'dept': dept, 'opkind': opkind, 'empID': empID, 'onboardDate': onboardDate,
                 'birthday': birthday, 'job': job, 'mobile': mobile, 'household': household, 'contract': contract,
                 'contractTime': contractTime,'contractStart':contractStart,'contractEnd':contractEnd,
                 'workID': workID, 'sex': sex})

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

            employee.empID = aform.cleaned_data['empID']
            employee.dept = aform.cleaned_data['dept']
            employee.name = aform.cleaned_data['name']
            employee.sex = aform.cleaned_data['sex']
            employee.dept = aform.cleaned_data['dept']
            employee.name = aform.cleaned_data['name']
            employee.birthday = aform.cleaned_data['birthday']

            employee.workID = aform.cleaned_data['workID']
            employee.job = aform.cleaned_data['job']
            employee.section = aform.cleaned_data['section']
            employee.process = aform.cleaned_data['process']
            employee.jobType = aform.cleaned_data['jobType']
            employee.jobTitle = aform.cleaned_data['jobTitle']
            employee.mobile = aform.cleaned_data['mobile']

            employee.household = aform.cleaned_data['household']
            employee.householdType = aform.cleaned_data['householdType']
            employee.nation = aform.cleaned_data['nation']
            employee.political = aform.cleaned_data['political']
            employee.firstWorkDate = aform.cleaned_data['firstWorkDate']
            employee.onboardDate = aform.cleaned_data['onboardDate']
            employee.education = aform.cleaned_data['education']

            employee.degree = aform.cleaned_data['degree']
            employee.graduateDate = aform.cleaned_data['graduateDate']
            employee.educationType = aform.cleaned_data['educationType']
            employee.specialty = aform.cleaned_data['specialty']
            employee.foreignLanguage = aform.cleaned_data['foreignLanguage']
            employee.labor = aform.cleaned_data['labor']
            employee.contract = aform.cleaned_data['contract']

            employee.contractTime = aform.cleaned_data['contractTime']
            employee.contractStart = aform.cleaned_data['contractStart']
            employee.contractEnd = aform.cleaned_data['contractEnd']
            employee.technicalTitle = aform.cleaned_data['technicalTitle']
            employee.technicalName = aform.cleaned_data['technicalName']
            employee.workerLevel = aform.cleaned_data['workerLevel']
            employee.homeAddress = aform.cleaned_data['homeAddress']

            employee.certificate = aform.cleaned_data['certificate']
            employee.medicalResult = aform.cleaned_data['medicalResult']

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
