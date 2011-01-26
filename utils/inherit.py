"""
This module uses the django snippets 'Model inheritance with content type and
inheritance aware manager' (http://djangosnippets.org/snippets/1034/).

Using this module, instances of a model class and its subclasses can be accessed by the objects manager of the super class.

Usage:

from django.db import models
from django.contrib.contenttypes.models import ContentType
from djity.utils import SuperManager

class SuperClass(models.Model):
    content_type = models.ForeignKey(ContentType,editable=False,null=True)
    objects = SuperManager()
	# other fields and methods...
	
	def save(self,*args,**kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
            super(SuperClass,self).save(*args,**kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == SuperClass):
            return self
        return model.objects.get(id=self.id)

class SubClass(SuperClass):
    objects = SuperManager()

"""

from django.db import models
from django.db.models.query import QuerySet

class SubclassingQuerySet(QuerySet):
    def __getitem__(self,k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result,models.Model):
            return result.as_leaf_class()
        else:
            return result

    def __iter__(self):
        for item in super(SubclassingQuerySet,self).__iter__():
            yield item.as_leaf_class()


class SuperManager(models.Manager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)
