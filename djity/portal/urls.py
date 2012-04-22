from django.conf.urls.defaults import *

from django.contrib import admin

admin.autodiscover()

#from djity.core import portal,projects
from djity.project.urls import urlpatterns as project_urls

urlpatterns = patterns('djity.portal.views',
    # Standard djityportal pages, independant from projects and modules
    url(r'admin/',include(admin.site.urls)),

    # all other urls are handled by djity.projects
    (r'^',include(project_urls)),
)
