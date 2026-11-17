"""
URL configuration for todo_web_cite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.urls import reverse_lazy

from app.views import register, task_by_id, task_detail, task_list, tasks


urlpatterns = [
    path('', task_list, name='task_list'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(next_page=reverse_lazy('task_list')), name='login'),
    path('accounts/register/', register, name='register'),
    path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('api/v1/tasks/', tasks, name='tasks'),
    path('api/v1/tasks/<int:pk>/', task_by_id, name='task_by_id'),
]
