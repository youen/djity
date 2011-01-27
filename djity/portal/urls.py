from django.conf.urls.defaults import *

#from djity.core import portal,projects
from djity.core.project.urls import urlpatterns as project_urls

urlpatterns = patterns('djity.core.portal.views',
    # Standard djityportal pages, independant from projects and modules
    (r'^accounts/register/$','register'),
    (r'^accounts/profile/$','profile'),
    #(r'^legal/$','legal'),
    # etc...

    # all other urls are handled by djity.projects
    (r'^',include(project_urls)),
)
