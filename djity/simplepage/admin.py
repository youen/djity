from djity.simplepage.models import SimplePage
from django.contrib import admin
from djity.project.admin import register, DjityModelAdmin, ModuleModelAdmin

register(SimplePage,ModuleModelAdmin)

