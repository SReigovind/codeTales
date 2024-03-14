"""
URL configuration for codetales_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('about/', views.about ,name='about'),
    path('feedback/', views.feedback ,name='feedback'),
    path('course/', views.course ,name='course'),
    path('courses/', views.courses ,name='courses'),
    path('reglog/',views.reglog,name='reglog'),
    path('profile/',views.profile,name='profile'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminprofile/',views.adminprofile,name='adminprofile'),
    path('adminfeedback/',views.adminfeedback,name='adminfeedback'),
    path('deleteprofile/<int:id>',views.deleteprofile,name='deleteprofile'),
    path('adminhomepage/',views.adminhomepage,name='adminhomepage'),
    path('profileupdate/',views.profileupdate,name='profileupdate'),
    path('homepage/',views.homepage,name='homepage'),
    path('bookpage/<str:corp>,<int:level>,<int:page>',views.bookpage,name='bookpage'),
    path('clevel/',views.clevel,name='clevel'),
    path('plevel/',views.plevel,name='plevel'),
    path('code/<str:language>,<int:puzzleid>',views.code,name='code'),

]
