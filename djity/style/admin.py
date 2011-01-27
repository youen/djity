from django.contrib import admin
from djity.core.style.models import CSS

class CSSAdmin(admin.ModelAdmin):
    pass

admin.site.register(CSS, CSSAdmin)
    
