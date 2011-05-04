from django.conf.urls.defaults import *

from djity.simplepage.urls import urlpatterns as simplepage_urls
from djity.style.urls import urlpatterns as css_urls
from djity.utils import djity_modules

from django.utils.importlib import import_module
from django.conf import settings

from django.db.models.loading import get_models

redirected_url = patterns('',
        url(r'^(?P<path>[-\w]+(/[-\w]*)?)','djity.portal.views.redirect_root',name='redirect_root'),
)

portal_urls = patterns('',
        url(r'^login/*$','djity.project.views.login',name='login'),
        url(r'^forbidden/*$','djity.project.views.forbidden',name='forbidden'),
)

urlpatterns = patterns('',
    (r'^/*$',include(redirected_url),{'project_name':'root'}),
)


for app in settings.DJITY_APPS:
    app_url = import_module('%s.urls'%app)
    urlpatterns += patterns('',
                (r'^(?P<project_name>[-\w]+)/%s/*'%app_url.prefix,include(app_url)),
    )

urlpatterns += patterns('',
    # project page redirect to the first tab
    url(r'^(?P<project_name>[-\w]+)/*$','djity.project.views.first_tab',name='first_tab'),
    # login view as a pseudo application
    (r'^(?P<project_name>[-\w]+)/',include(portal_urls)),
    # all other urls are handled by djity.modules.simple_page
    (r'^(?P<project_name>[-\w]+)/css/',include(css_urls)),
    (r'^(?P<project_name>[-\w]+)/+',include(simplepage_urls)),
)


