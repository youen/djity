# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings 
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from djity.transmeta import TransMeta
from djity.portlet.models import TextPortlet,update_portlets_context

class SiteRoot(models.Model):
    """
    Root of a Djity Website

    # Create a Site
    >>> site = SiteRoot.objects.create(label = 'root', name = 'djity', presentation = 'une presentation')
    """

    label = models.CharField("label", max_length=4, default=_("home"))
    name =  models.TextField()
    presentation =  models.TextField()
    portlets = generic.GenericRelation('portlet.Portlet')

    def save(self,*args,**kwargs):
        """
        If a site root is new init its dependances
        """
        new = False
        if self.id == None:
            new = True
        
        if new:
            from djity.project.models import Project
            root_project = Project(name="root",label=settings.ROOT_PROJECT_LABEL,description="Djity portal instance root project",is_root=True)
            root_project.save()
            site_name = ""
            site_presentation = ""
            self.name,self.presentation = site_name,site_presentation
        
        super(SiteRoot,self).save(*args,**kwargs)

        if new:
            pass

    def update_context(self,context):
        """
        Provide a context for all portal templates or sub templates
        """
        context.update({
            'site_name':self.name,
            'MEDIA_URL':settings.MEDIA_URL,
        })

        # Add context of site root level portlets
        update_portlets_context(self,context)

    def __unicode__(self):
        return self.name


  
class UserProfile(models.Model):
        user = models.OneToOneField(User)
        activation_key = models.CharField(max_length=40)
        key_expires = models.DateTimeField()


