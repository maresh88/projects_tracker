from django.urls import path

from projects import views

app_name = 'projects'

urlpatterns = [
    path('filter/', views.ProjectFilterView.as_view(), name='filter'),
    path('<int:pk>/<slug:slug>/', views.ProjectDetailView.as_view(), name='detail'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('update/<int:pk>/<slug:slug>/', views.ProjectUpdateView.as_view(), name='update'),
    path('', views.ProjectsListView.as_view(), name='projects'),
]
