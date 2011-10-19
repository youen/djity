from django.conf.urls.defaults import *
from djity.search.views import project_search

urlpatterns = patterns('djity.search.views',
    url(r'^$', project_search, name='project_search'),
)
