from django.contrib import admin
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectsListView.as_view(), name='projects_list'),
]
