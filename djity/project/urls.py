# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from django.conf.urls.defaults import *

from djity.simplepage.urls import urlpatterns as simplepage_urls
from djity.style.urls import urlpatterns as css_urls
from djity.search.urls import urlpatterns as search_urls
from djity.utils import djity_modules

from djity.project.admin import get_url as admin_urls
from django.utils.importlib import import_module
from django.conf import settings

from django.db.models.loading import get_models


portal_urls = patterns('',
        url(r'^login/*$','djity.project.views.login',name='login'),
        url(r'^forbidden/*$','djity.project.views.forbidden',name='forbidden'),

)

urlpatterns = patterns('',
    # project page redirect to the first tab
    url(r'^(?P<project_name>[-\w]+)/*$','djity.project.views.first_tab',name='first_tab'),
    # login and navigation views as a pseudo applications
    (r'^(?P<project_name>[-\w]+)/',include(portal_urls)),
    # css as a pseudo application too
    (r'^(?P<project_name>[-\w]+)/css/',include(css_urls)),
    # and search also
    (r'^(?P<project_name>[-\w]+)/search/',include(search_urls)),
    # and search also
    (r'^(?P<project_name>[-\w]+)/admin/',include(admin_urls())),
)

#import urls from djity applications
for app in settings.DJITY_APPS:
    app_url = import_module('%s.urls'%app)
    urlpatterns += patterns('',
                (r'^(?P<project_name>[-\w]+)/%s/+'%app_url.prefix,include(app_url)),
    )

#redirect to a simple or the root project
urlpatterns += patterns('',
        (r'^(?P<project_name>[-\w]+)/+',include(simplepage_urls)),
        url(r'^(?P<path>[-\w]*)','djity.portal.views.redirect_root',name='redirect_root'),
)
