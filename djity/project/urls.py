from django.conf.urls.defaults import *

from djity.simplepage.urls import urlpatterns as simplepage_urls
from djity.style.urls import urlpatterns as css_urls
from djity.utils import djity_modules

from django.utils.importlib import import_module
from django.conf import settings

from django.db.models.loading import get_models

redirected_url = patterns('',
        url(r'^(?P<path>.*)','djity.portal.views.redirect_root',name='redirect_root'),
)

account_urls = patterns('',
        url(r'^','djity.project.views.login',name='login'),
)

urlpatterns = patterns('',

	# Root project urls
    (r'^root/css/',include(css_urls),{'project_name':'root'}),
	(r'^root/',include(redirected_url),{'project_name':'root'}),
	(r'^root',include(redirected_url),{'project_name':'root'}),
    (r'^css/',include(css_urls),{'project_name':'root'}),
	(r'^login/',include(account_urls),{'project_name':'root'}),
)

for app in settings.DJITY_APPS:
    app_url = import_module('%s.urls'%app)
    urlpatterns += patterns('',
            (r'^%s/'%app_url.prefix,include(app_url),{'project_name':'root'}),
    )

urlpatterns += patterns('',
		(r'^$','djity.project.views.first_tab',{'project_name':'root'}),
		(r'^/$','djity.project.views.first_tab',{'project_name':'root'}),

    (r'^/',include(simplepage_urls),{'project_name':'root'}),
    (r'^',include(simplepage_urls),{'project_name':'root'}),
	# etc...
    (r'^(?P<project_name>[-\w]+)/css/',include(css_urls)),
    (r'^(?P<project_name>[-\w]+)/login/',include(account_urls)),
)

for app in settings.DJITY_APPS:
    app_url = import_module('%s.urls'%app)
    urlpatterns += patterns('',
                (r'^(?P<project_name>[-\w]+)/%s/'%app_url.prefix,include(app_url)),
    )

# project page redirect to the first tab
urlpatterns += patterns('',
		(r'^(?P<project_name>[-\w]+)$','djity.project.views.first_tab'),
		(r'^(?P<project_name>[-\w]+)/$','djity.project.views.first_tab'),
	)

# all other urls are handled by djity.modules.simple_page
urlpatterns += patterns('',
    (r'^(?P<project_name>[-\w]+)',include(simplepage_urls)),
    (r'^(?P<project_name>[-\w]+)/',include(simplepage_urls)),)


