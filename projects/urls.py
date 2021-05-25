from django.contrib import admin
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('search/reporter/', views.search_reporter, name='search_reporter'),
    path('filter/', views.ProjectFilterView.as_view(), name='filter'),
    path('<int:pk>/<slug:slug>/', views.ProjectDetailView.as_view(), name='detail'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('update/<int:pk>/<slug:slug>/', views.ProjectUpdateView.as_view(), name='update'),
    path('', views.ProjectsListView.as_view(), name='projects'),
]
