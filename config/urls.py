import debug_toolbar

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('projects.urls', namespace='projects')),

    path('__debug__/', include(debug_toolbar.urls)),
]

