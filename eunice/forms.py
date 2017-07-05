from django import forms

SEX_CHOICES = (('男', '男'), ('女', '女'))


class VideoForm(forms.Form):
    empID = forms.CharField(initial='',label='身份证号')
    dept = forms.CharField(initial='',label='部门')
    name = forms.CharField(initial='xxx',label='姓名')
    workID = forms.CharField(initial='',label='工号')
    job = forms.CharField(initial='',label='岗位')
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=SEX_CHOICES, label="性别")
    birthday = forms.DateField(widget=forms.SelectDateWidget(),label='出生年月')
