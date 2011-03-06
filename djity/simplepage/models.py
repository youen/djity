from django.db import models
from django.contrib.contenttypes import generic
from tinymce.models import HTMLField
from djity.utils import djreverse
from djity.project.models import Module
from djity.portlet.models import TemplatePortlet
#from djity.services.revtext.field import RevField
from djity.transmeta import TransMeta
#from djity.services.lod import *
#from djity.services.partner.models import AmazonBlendedPortlet


from djity.utils.inherit import SuperManager

class SimplePage(Module):
    """
    Wiki module for djity
    """
    objects = SuperManager()

    content = HTMLField()

    __metaclass__ = TransMeta

    def save(self,*args,**kwargs):
        """
        After some change this function is empty
        just conserved it for lazy devlopers
        """
        if self.id == None:
            super(SimplePage,self).save(*args, **kwargs)

        else:
            super(SimplePage,self).save(*args, **kwargs)

    def delete(self,*args,**kwargs):
        for tp in TemplatePortlet.objects.filter(container_id=self.id):
            tp.delete() 
        super(SimplePage,self).delete(*args, **kwargs)
            
    def subnav(self,project_name):
        """
        return sub navigation list
        """
        return []

    def djity_url(self,context):
        """
        Return the module's start page
        """
        return djreverse('simplepage-view',context,module_name=self.name)

    class Meta:
        translate = ('content',)
