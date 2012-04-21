from models import TextPortlet,TemplatePortlet
from django.contrib import admin
from djity.project.admin import register, DjityModelAdmin
from django.contrib.contenttypes.models import ContentType

class ContainerModelAdmin(DjityModelAdmin):
    
    def __init__(self,*args,**kwarg):
        super(ContainerModelAdmin,self).__init__(*args,**kwarg)
        project_type = ContentType.objects.get_for_model(self._project)

        self.objects_filter = {
                               'container_type__pk':project_type.id,
                               'container_id':self._project.id
                               }

    
register(TextPortlet,ContainerModelAdmin)
register(TemplatePortlet,ContainerModelAdmin)
