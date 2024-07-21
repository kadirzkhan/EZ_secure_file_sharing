"""
URL configuration for secure_file_sharing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# filesharing/urls.py
from django.urls import path
from secure_file_sharing import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    
    path('', views.ops_login, name='ops_login'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('client-signup/', views.client_signup, name='client_signup'),
    path('verify-email/<str:code>/', views.verify_email, name='verify_email'),
    path('client-login/', views.client_login, name='client_login'),
    path('list-files/', views.list_files, name='list_files'),
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),
] 
