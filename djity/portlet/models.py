from django.db import models
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.loader import render_to_string

from djity.utils.inherit import SuperManager
from djity.transmeta import TransMeta

class Portlet(models.Model):
    """
    Portlet super class, use as abstract
    """
    # For powerful inheritance use content type
    content_type = models.ForeignKey(ContentType,editable=False,null=True)
    objects = SuperManager()

    # Generic key to a portlet container (can be a project, a module
    # connection,etc..)
    container_type = models.ForeignKey(ContentType,related_name="portlet_container_type")
    container_id = models.PositiveIntegerField()
    container = generic.GenericForeignKey(ct_field='container_type',fk_field='container_id')

    # position of the portlet in the template, can be 'top','bottom','left' or 'right'
    position = models.CharField("position",max_length=200)
    # position relative to other portlets that have same position value
    # If a portlet has a lower value than another one it will be displayed on top
    # If a portlet has a value of -1 it will always be on top
    # If a portlet has a value of 10 it will always be at the bottom
    # Other values should always be positive
    rel_position = models.IntegerField("relative position",default=1)
    # should the portlet be displayed
    is_active = models.BooleanField('is active', default=True,
        help_text="if disabled this portlet won't be displayed in the container")

    div_class = models.CharField("style",max_length=200,default="dj-editable ui-widget ui-widget-content ui-corner-all")
    
    onload = ""
    media = set()

    def save(self,*args,**kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Portlet,self).save(*args,**kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Portlet):
            return self
        return model.objects.get(id=self.id)
    

class TextPortlet(Portlet):
    """
    A simple portlet displaying some text
    """
    
    __metaclass__ = TransMeta
    
    objects = SuperManager()

    content = models.TextField("content")


    def render(self,context):
        context["portlet"] = self
        return render_to_string("djity/portlet/text_portlet.html",context)

    def __unicode__(self):
        return _(u"TextPortlet: %s")% self.content

    class Meta:
        translate = ('content',)

class TemplatePortlet(Portlet):
    """
    A simple portlet that renders a template with current context

    The template for this portlet should extend 'core/portlet/portlet.html'
    """
    objects = SuperManager()

    template = models.CharField("template",max_length=200)
    onload = models.CharField("onload",max_length=200,default="")

    def render(self,context):
        context["portlet"] = self
        return render_to_string(self.template,context)
    
    def __unicode__(self):
        return _(u"TemplatePortlet: %s") % self.template

def get_portlets(container):
    """
    Access all portlets associated to a given container
    """
    ctype = ContentType.objects.get_for_model(container)
    portlets = Portlet.objects.filter(container_type__pk=ctype.id, container_id=container.id)
    return portlets

def get_portlets_data(container,position,parent_context):
    """
    Build context for all portlets for a container and at a given postion (left, right, etc..)
    """
    ctype = ContentType.objects.get_for_model(container)
    portlets = Portlet.objects.filter(container_type__pk=ctype.id, container_id=container.id,position=position)
    portlets.order_by('rel_position')
    data = {}
    portlet_ids = []
    data['onload'] = parent_context.get('onload',"")
    data['media'] = parent_context.get('media',set([]))
    for portlet in portlets:
        # remember each portlet and put it in al list
        portlet_id = portlet.id
        data["portlet_%s"%portlet_id] = portlet
        portlet_ids.append(portlet_id)
        # add onload code
        data['onload'] += portlet.onload
        data['media'] |= portlet.media

    pos_key = "portlets_%s"%position
    data[pos_key] = parent_context.get(pos_key,[])
    data[pos_key].extend(portlet_ids)
    return data

def update_portlets_context(container, context):
    """
    Build the context dicitonary containing all portlets data for a container
    """
    for position in ['left','right','bottom','top','toolbar']:
        context.update(get_portlets_data(container,position,context))

    return context

