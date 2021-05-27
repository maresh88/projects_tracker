from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Profile


admin.site.register(Profile, MPTTModelAdmin)
