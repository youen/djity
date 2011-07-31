from haystack import indexes

from djity.simplepage.models import SimplePage

class SimplePageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='content')
    project = indexes.CharField(model_attr='project')

    def get_model(self):
        return SimplePage
