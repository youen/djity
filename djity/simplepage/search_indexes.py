from haystack.indexes import *
from haystack import site

from djity.simplepage.models import SimplePage

class SimplePageIndex(SearchIndex):
    text = CharField(document=True, model_attr='content')
    project = CharField(model_attr='project')

site.register(SimplePage, SimplePageIndex)
