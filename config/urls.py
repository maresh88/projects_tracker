import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from projects.views import ProjectsListView

urlpatterns = [
    path('profiles/', include('profiles.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls', namespace='projects')),
    path('', ProjectsListView.as_view(), name='homepage'),

    # debug_toolbar
    path('__debug__/', include(debug_toolbar.urls)),
]

