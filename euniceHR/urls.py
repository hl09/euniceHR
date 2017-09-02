"""WateringTools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from eunice.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [url(r'^showgrid/$',showgrid),url(r'^$',employeeList),url(r'^leave/$', leave),url(r'^delete/$', delete),url(r'^weekreport/$', weekReport),url(r'^statistical/$', statistical),url(r'^saveemployee/$', saveEmployee),url(r'^showmodify/$', showModify), url(r'^search/$', search), url(r'^index/$',employeeList)] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT)
