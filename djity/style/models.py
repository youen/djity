import os, json
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
        self.set_all_values(self._default_style)

    def set_all_values(self,style):
        """
        Set all values using a dictionary

        Used by set_to_default, to inherit the style of another project or to
        allow the user to apply a full theme at once
        """
        self.__dict__.update(style)
        self.save()

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

    def get_values(self):
        values = []
        for name,value in self._default_style + [('extra','')]:
            values.append((name,self.__dict__[name]))
        return values

    def get_context(self):
        """
        Return all fields for the stylesheet template
        """
        context = dict(self.get_values())
        context['textures'] = self.get_textures()
        return context

"""
class ProjectCSS(CSS,models.Model):
    __metaclass__ = MetaCSS
    _default_style = settings.DEFAULT_PORTAL_STYLE

class UICSS(CSS,models.Model):
    __metaclass__ = MetaCSS
    _default_style = settings.DEFAULT_UI_STYLE
"""
