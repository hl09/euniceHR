from django import forms

SEX_CHOICES = (('男', '男'), ('女', '女'))
DEPT_CHOICES = (
('技术', '技术'), ('制造', '制造'), ('质保', '质保'), ('综合办', '综合办'), ('制造-物流', '制造-物流'), ('财务', '财务'), ('商务', '商务'),
('安监室', '安监室'))
JOB_CHOICES = (('工程技术人员','工程技术人员'),('管理人员','管理人员'),('间接生产工人','间接生产工人'),('直接生产工人','直接生产工人'))
EMPTYPE_CHOICES= (('在岗职工', '在岗职工'), ('市内劳务工', '市内劳务工'))

class VideoForm(forms.Form):
    empID = forms.CharField(initial='', label='身份证号', required=True,error_messages={'required': '身份证号不能为空.'})
    dept = forms.ChoiceField(choices=DEPT_CHOICES, label='部门', required=True,error_messages={'required': '部门不能为空.'})
    name = forms.CharField(initial='', label='姓名', required=True,error_messages={'required': '姓名不能为空.'})
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=SEX_CHOICES, label="性别",required=True,error_messages={'required': '性别不能为空.'})
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'easyui-datebox'}))
    workID = forms.CharField(initial='', label='工号', required=True,
                             error_messages={'required': "工号不能为空"})
    job = forms.CharField(initial='', label='岗位',required=True,
                             error_messages={'required': "岗位不能为空"})

    section = forms.CharField(initial='', label='工段',required=False)

    team = forms.CharField(initial='', label='班组', required=False)
    process = forms.CharField(initial='', label='边缘工序', required=False)
    jobType = forms.ChoiceField(choices=JOB_CHOICES,label='岗位分类',required=False)
    employType = forms.ChoiceField(choices=EMPTYPE_CHOICES, label='用工性质', required=False)
    jobTitle = forms.CharField(initial='', label='职务', required=False)
    mobile = forms.CharField(initial='', label='移动电话', required=False)
    household = forms.CharField(initial='', label='户口所在地', required=False)
    householdType = forms.CharField(initial='', label='户口性质', required=False)
    nation = forms.CharField(initial='', label='民族', required=False)
    political = forms.CharField(initial='', label='政治面貌', required=False)
    firstWorkDate = forms.CharField(initial='', label='参加工作时间', required=False)
    onboardDate = forms.CharField(widget=forms.DateInput(attrs={'class': 'easyui-datebox'}), label='进本单位日期',
                                  required=True,
                                  error_messages={'required': "日期不能为空"})
    education = forms.CharField(initial='', label='学历', required=False)
    degree = forms.CharField(initial='', label='学位', required=False)
    graduateDate = forms.CharField(initial='', label='毕<肄>业年月', required=False)
    educationType = forms.CharField(initial='', label='学习形式', required=False)
    university = forms.CharField(initial='', label='毕<肄>业学校', required=False)
    specialty = forms.CharField(initial='', label='所学专业', required=False)
    foreignLanguage = forms.CharField(initial='', label='掌握语种及语种级别', required=False)
    labor = forms.CharField(initial='', label='劳务公司', required=False)
    contract = forms.CharField(initial='', label='合同制形式', required=False)
    contractTime = forms.CharField(initial='', label='合同年限', required=False)
    contractStart = forms.DateField(widget=forms.DateInput(attrs={'class': 'easyui-datebox'}), label='合同开始日期',
                                    required=True,
                                    error_messages={'required': "开始日期不能为空"})
    contractEnd = forms.DateField(widget=forms.DateInput(attrs={'class': 'easyui-datebox'}), label='合同结束日期',
                                  required=True,
                                  error_messages={'required': "结束日期不能为空"})
    technicalTitle = forms.CharField(initial='', label='专业技术等级', required=False)
    technicalName = forms.CharField(initial='', label='专技职务资格名称', required=False)
    workerLevel = forms.CharField(initial='', label='工人技术等级', required=False)
    homeAddress = forms.CharField(initial='', label='家庭地址', required=False)
    certificate = forms.CharField(initial='', label='上岗证', required=False)

    medicalResult = forms.CharField(initial='', label='体检结果', required=False)

    flag = forms.CharField(initial='O', label='标记', required=False)

    opkind = forms.CharField(initial='', label='opkind',required=False)

