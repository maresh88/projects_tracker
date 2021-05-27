from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('search/reporter/', views.search_reporter, name='search_reporter'),
]