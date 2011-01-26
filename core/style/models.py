import os
from django.db import models
from django.conf import settings

class MetaCSS(models.base.ModelBase):
    """
    Metaclass to dynamically create editable css fields from settings
    """
    def __new__(cls,name,bases,attrs):

        default_style = attrs['_default_style']

        for key,value in default_style:
            # create a char field for all item in the default style
            attrs[key] = models.CharField(key.replace('_',' '),max_length=200)
        # create a text field for extra css code
        attrs['extra'] = models.TextField('extra',default=' ')

        return super(MetaCSS,cls).__new__(cls,name,bases,attrs)

class CSS(models.Model):
    """
    Generic class for CSS stylesheet templates.

    A class inheriting CSS must have an attribute _default_style as a list of tuples ('fieldname','value')
    """ 

    __metaclass__ = MetaCSS
    _default_style = settings.DEFAULT_STYLE

    def set_to_default(self):
        """
        Set default values from settings
        """
        for name,value in self._default_style:
            self.__dict__[name] = value

    def save(self,*args,**kwargs):
        """
        Check if a CSS instance is new and set fields values to default if it is
        """
        #Is this a new instance of CSS ?
        new = False
        if self.id == None:
            new = True

        super(CSS,self).save(*args, **kwargs)

        if new:
            self.set_to_default()
        
        super(CSS,self).save(*args, **kwargs)

    def get_textures(self):
        """
        Check djity's textures directory for available textures
        """
        textures = os.listdir(settings.TEXTURES_DIR)
        textures = [t for t in textures if t.endswith('.png')]
        textures = sorted(textures, key=lambda t:int(t.split('_')[0]))
        return textures

    def get_context(self):
        """
        Return all fields for the stylesheet template
        """
        context = {}
        for name,value in self._default_style + [('extra','')]:
            context[name] = self.__dict__[name]

        context['textures'] = self.get_textures()

        return context

    def serialize(self):
        """
        Return a list of attributes compatible with the one in settings.py
        """
        ret = "[\n"
        for name,value in self._default_style:
            value = self.__dict__[name]
            value = value.replace("\"","\\\"")
            ret += "\t(\"%s\",r\"%s\"),\n" % (name,value)
        ret += "]"

        return ret

"""
class ProjectCSS(CSS,models.Model):
    __metaclass__ = MetaCSS
    _default_style = settings.DEFAULT_PORTAL_STYLE

class UICSS(CSS,models.Model):
    __metaclass__ = MetaCSS
    _default_style = settings.DEFAULT_UI_STYLE
"""
