from django.conf.urls.defaults import *

from djity.core.simplepage.urls import urlpatterns as simplepage_urls
from djity.core.style.urls import urlpatterns as css_urls
from djity.modules.wiki.urls import urlpatterns as wiki_urls
from djity.modules.repository.urls import urlpatterns as repo_urls
from djity.modules.quizz.urls import urlpatterns as quizz_urls
from djity.modules.blog.urls import urlpatterns as blog_urls
from djity.utils import djity_modules

import imp
from django.utils.importlib import import_module
from django.conf import settings

from django.db.models.loading import get_models

redirected_url = patterns('django.views.generic.simple',
        (r'^(?P<path>.*)','redirect_to',{'url':'/%(path)s'}),
)

urlpatterns = patterns('',

	# Root project urls
    (r'^root/css/',include(css_urls),{'project_name':'root'}),
	(r'^root/',include(redirected_url),{'project_name':'root'}),
	(r'^root',include(redirected_url),{'project_name':'root'}),
    (r'^css/',include(css_urls),{'project_name':'root'}),
)

for app in settings.DJITY_MODULES:
    url = import_module('%s.urls'%app)
    urlpatterns += patterns('',
            (r'^%s/'%app.split('.')[-1],include(url),{'project_name':'root'}),
    )

urlpatterns += patterns('',
    (r'^/',include(simplepage_urls),{'project_name':'root'}),
    (r'^',include(simplepage_urls),{'project_name':'root'}),
	# etc...
    (r'^(?P<project_name>[-\w]+)/css/',include(css_urls)),
)

for app in settings.DJITY_MODULES:
    url = import_module('%s.urls'%app)
    urlpatterns += patterns('',
                (r'^(?P<project_name>[-\w]+)/%s/'%app.split('.')[-1],include(url)),
    )

# all other urls are handled by djity.modules.simple_page
urlpatterns += patterns('',
    (r'^(?P<project_name>[-\w]+)',include(simplepage_urls)),
    (r'^(?P<project_name>[-\w]+)/',include(simplepage_urls)),)


