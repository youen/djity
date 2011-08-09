from django.conf import settings

from haystack import indexes

from djity.simplepage.models import SimplePage

class SimplePageIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='content')
    project = indexes.IntegerField(model_attr='project__id')
    status = indexes.MultiValueField()

    def prepare_status(self,obj):
        return range(obj.status+1)

    def get_model(self):
        return SimplePage
