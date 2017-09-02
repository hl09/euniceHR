from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from .forms import *
from eunice import models
from django.db.models import Q
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
    aList = models.Employee.objects.filter(flag='O')

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
        workbook.Worksheets('Sheet1').Cells(i, 2).Value = aItem.dept
        workbook.Worksheets('Sheet1').Cells(i, 3).Value = aItem.name
        workbook.Worksheets('Sheet1').Cells(i, 4).Value = aItem.workID
        workbook.Worksheets('Sheet1').Cells(i, 5).Value = aItem.job
        workbook.Worksheets('Sheet1').Cells(i, 6).Value = aItem.section
        workbook.Worksheets('Sheet1').Cells(i, 7).Value = aItem.team
        workbook.Worksheets('Sheet1').Cells(i, 8).Value = aItem.process
        workbook.Worksheets('Sheet1').Cells(i, 9).Value = aItem.jobType
        workbook.Worksheets('Sheet1').Cells(i, 10).Value = aItem.employType
        workbook.Worksheets('Sheet1').Cells(i, 11).Value = aItem.jobTitle
        workbook.Worksheets('Sheet1').Cells(i, 12).Value = aItem.empID
        workbook.Worksheets('Sheet1').Cells(i, 13).Value = aItem.sex
        workbook.Worksheets('Sheet1').Cells(i, 14).Value = str(aItem.birthday)

        workbook.Worksheets('Sheet1').Cells(i, 17).Value = aItem.mobile
        workbook.Worksheets('Sheet1').Cells(i, 18).Value = aItem.household
        workbook.Worksheets('Sheet1').Cells(i, 19).Value = aItem.householdType
        workbook.Worksheets('Sheet1').Cells(i, 20).Value = aItem.nation
        workbook.Worksheets('Sheet1').Cells(i, 21).Value = aItem.political
        workbook.Worksheets('Sheet1').Cells(i, 22).Value = aItem.firstWorkDate
        workbook.Worksheets('Sheet1').Cells(i, 23).Value = aItem.onboardDate

        workbook.Worksheets('Sheet1').Cells(i, 25).Value = aItem.education
        workbook.Worksheets('Sheet1').Cells(i, 26).Value = aItem.degree
        workbook.Worksheets('Sheet1').Cells(i, 27).Value = aItem.graduateDate
        workbook.Worksheets('Sheet1').Cells(i, 28).Value = aItem.educationType
        workbook.Worksheets('Sheet1').Cells(i, 29).Value = aItem.university
        workbook.Worksheets('Sheet1').Cells(i, 30).Value = aItem.specialty
        workbook.Worksheets('Sheet1').Cells(i, 31).Value = aItem.foreignLanguage
        workbook.Worksheets('Sheet1').Cells(i, 32).Value = aItem.labor
        workbook.Worksheets('Sheet1').Cells(i, 33).Value = aItem.contract
        workbook.Worksheets('Sheet1').Cells(i, 34).Value = aItem.contractTime
        workbook.Worksheets('Sheet1').Cells(i, 35).Value = str(aItem.contractStart)
        workbook.Worksheets('Sheet1').Cells(i, 36).Value = str(aItem.contractEnd)
        workbook.Worksheets('Sheet1').Cells(i, 37).Value = aItem.technicalTitle
        workbook.Worksheets('Sheet1').Cells(i, 38).Value = aItem.technicalName
        workbook.Worksheets('Sheet1').Cells(i, 39).Value = aItem.workerLevel
        workbook.Worksheets('Sheet1').Cells(i, 40).Value = aItem.homeAddress
        workbook.Worksheets('Sheet1').Cells(i, 41).Value = aItem.certificate
        workbook.Worksheets('Sheet1').Cells(i, 42).Value = aItem.medicalResult
        if i > 5:
            break

    sht = workbook.Worksheets('Sheet1')
    for j in range(i + 1, 1001):
        sht.Rows(i + 1).Delete()

    workbook.SaveAs(r'D:\weekreport_wh.xlsx')
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
            query = models.Employee.objects.filter(dept=dept, flag='O')
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
        # export to excel
        try:
            pythoncom.CoInitialize()
            excel_app = wc.Dispatch('Excel.Application')
            workbook = excel_app.Workbooks.open(r'D:\pythonTraining\euniceHR\static\2.xlsx')
            i = 2
            for aSumItem in beanList:
                workbook.Worksheets('Sheet1').Cells(i, 1).Value = aSumItem.deptName
                workbook.Worksheets('Sheet1').Cells(i, 2).Value = aSumItem.gc
                workbook.Worksheets('Sheet1').Cells(i, 3).Value = aSumItem.gl
                workbook.Worksheets('Sheet1').Cells(i, 4).Value = aSumItem.jj
                workbook.Worksheets('Sheet1').Cells(i, 5).Value = aSumItem.zj
                workbook.Worksheets('Sheet1').Cells(i, 6).Value = aSumItem.zongji
                i = i + 1
            workbook.SaveAs(r'D:\statistical_wh.xlsx')
        except:
            print("导出excel失败！")
        finally:
            excel_app.Application.Quit()


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
        section = employee.section
        team = employee.team
        process = employee.process
        jobType = employee.jobType
        employType = employee.employType
        jobTitle = employee.jobTitle

        birthday = employee.birthday
        workID = employee.workID
        sex = employee.sex
        onboardDate = employee.onboardDate
        mobile = employee.mobile
        household = employee.household
        householdType = employee.householdType
        nation = employee.nation
        political = employee.political
        firstWorkDate = employee.firstWorkDate

        labor = employee.labor
        contract = employee.contract
        contractTime = employee.contractTime
        contractStart = employee.contractStart
        contractEnd = employee.contractEnd
        education = employee.education
        educationType = employee.educationType
        university = employee.university
        graduateDate = employee.graduateDate
        degree = employee.degree
        foreignLanguage = employee.foreignLanguage
        certificate = employee.certificate
        specialty = employee.specialty
        technicalTitle = employee.technicalTitle
        technicalName = employee.technicalName
        workerLevel = employee.workerLevel
        homeAddress = employee.homeAddress
        medicalResult = employee.medicalResult

        if employee:
            aform = VideoForm(
                {'name': name, 'dept': dept, 'opkind': opkind, 'empID': empID, 'onboardDate': onboardDate,
                 'birthday': birthday, 'job': job, 'mobile': mobile, 'household': household, 'labor': labor,
                 'contract': contract, 'team': team, 'process': process, 'jobType': jobType, 'employType': employType,
                 'jobTitle': jobTitle, 'contractTime': contractTime, 'contractStart': contractStart,
                 'contractEnd': contractEnd,
                 'workID': workID, 'sex': sex, 'section': section, 'medicalResult': medicalResult,
                 'homeAddress': homeAddress, 'workerLevel': workerLevel, 'technicalName': technicalName,
                 'technicalTitle': technicalTitle, 'specialty': specialty, 'certificate': certificate,
                 'firstWorkDate': firstWorkDate, 'political': political, 'nation': nation,
                 'foreignLanguage': foreignLanguage, 'degree': degree, 'graduateDate': graduateDate,
                 'university': university, 'education': education, 'educationType': educationType,
                 'householdType': householdType})

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
            employee.employType = aform.cleaned_data['employType']
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
            employee.flag = 'O'

            employee.save()

            # aList = models.Employee.objects.all()
            # return render(request, 'index.html', {'dataList': aList})
        else:
            return render(request, 'employee.html', {'form': aform})

    return HttpResponseRedirect('/index/')

#删除记录
def delete(request):
    if request.method == 'POST':
        checkboxlist = request.POST.getlist('checkboxlist')
        if checkboxlist:
            idstring = ','.join(checkboxlist)
            models.Employee.objects.extra(where=['id IN (' + idstring + ')']).delete()

    return HttpResponseRedirect('/index/')

#设置离职
def leave(request):
    if request.method == 'POST':
        checkboxlist = request.POST.getlist('checkboxlist')
        if checkboxlist:
            idstring = ','.join(checkboxlist)
            models.Employee.objects.extra(where=['id IN (' + idstring + ')']).update(flag = 'L')

    return HttpResponseRedirect('/index/')

def search(request):
    aList = models.Employee.objects.filter(flag='O')
    if request.POST:
        kwargs = {}

        sname = request.POST['searchName']
        sID = request.POST['searchID']
        sDept = request.POST['searchDept']
        sJob = request.POST['searchJob']
        sDate = request.POST['sDate']
        eDate = request.POST['eDate']
        sEmpID = request.POST['searchEmpID']
        sJobType = request.POST['searchJobType']
        sEmployType = request.POST['searchEmployType']
        sLeave = request.POST.getlist("searchLeave")

        if sname:
            kwargs['name'] = sname
        if sID:
            kwargs['workID'] = sID
        if sDept:
            kwargs['dept'] = sDept
        if sJob:
            kwargs['job'] = sJob
        if sEmpID:
            kwargs['empID'] = sEmpID
        if sJobType:
            kwargs['jobType'] = sJobType
        if sEmployType:
            kwargs['employType'] = sEmployType
        if sLeave:
            kwargs['flag'] = 'L'
            aList = models.Employee.objects.all()

        aList = aList.filter(**kwargs)

        if sDate:
            aList = aList.filter((Q(onboardDate__gte=sDate) & Q(onboardDate__lte=eDate)))

    return render(request, 'index.html', {'dataList': aList})
